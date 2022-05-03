#!/usr/bin/python3
import sys
import ipaddress
import json
import argparse
import yaml
import re
import socket
import ast
import signal
import textwrap
from time import sleep
sys.path.append('/opt/trex/current/automation/trex_control_plane/server/')
import outer_packages  # noqa: E402
from trex.stl.api import *  # noqa: E402


def get_nics_from_macs():
    """Get nic names from mac address

    It would look for files /sys/class/net/{nic}/address

    return nics: dict to get nic from mac.
    """
    nic_output = {}
    nics = socket.if_nameindex()
    nics = [list(nic)[1] for nic in nics]
    for nic in nics:
        with open('/sys/class/net/{}/address'.format(nic), 'r') as f:
            nic_output[f.read().rstrip('\r\n')] = nic
    return nic_output


def trex_cfg():
    """Get nics from trex cfg file

    Get nics from trex cfg file

    return devices: list with devices including  source and
                    destination macs
    """

    try:
        with open('/etc/trex_cfg.yaml', 'r') as stream:
            cfg_dict = yaml.safe_load(stream)
    except Exception as e:
        print(e)
        raise e

    nics = get_nics_from_macs()

    devices = []
    for val in cfg_dict[0]['port_info']:
        device = {}
        src_mac = val['src_mac']
        dst_mac = val['dest_mac']
        if src_mac in nics.keys():
            device['name'] = nics[src_mac]
        device['dest_mac'] = dst_mac
        device['src_mac'] = src_mac
        devices.append(device)
    return devices


def gen_scapy_pkt(devices, end_seq, proto, start_seq=0,
                  src_port=1025, dst_port=32768, direction=0):
    """Gen scapy packets

    It will generate packets for both interfaces. For one direction
    it will change source ip while for the other one it will change
    destination ip. All of the other ips/ports will remain constant.
    Each packet will have a different packet size so that it will be
    able to know the ip sent through the packet size. Testpmd is
    storing in the log packet size and queues information, but not
    ip address, so ip address is known through the packet size.
    source or destination ip that is changing will have this range:
    48.0.0.1 + start_seq until 48.0.0.1 + end_seq

    param devices: devices in which packets will be sent
    param end_seq: max seq number for packet generation
    param proto: UDP or TCP
    param start_seq: start seq number for packet generation
    param src_port: source port for all packets
    param dst_port: destination port for all packets
    param direction: packet direction (0 or 1)
    """
    ip_start = str(ipaddress.IPv4Address('48.0.0.1')+start_seq)
    size = 65
    iter = 0
    for i in range(start_seq, end_seq):
        print(str(ipaddress.IPv4Address(ip_start)+iter))
        pkt2 = Ether(src=devices[direction]['src_mac'],
                     dst=devices[direction]['dest_mac'])
        pkt1 = pkt2/IP(dst=str(ipaddress.IPv4Address(ip_start)+iter),
                       src="16.0.0.1")
        dport = dst_port
        sport = src_port
        if direction == 1:
            pkt1 = pkt2/IP(src=str(ipaddress.IPv4Address(ip_start)+iter),
                           dst="16.0.0.1")
            dport = src_port
            sport = dst_port
        if proto == 'UDP':
            pkt = pkt1/UDP(dport=dport, sport=sport)
        else:
            pkt = pkt1/TCP(dport=dport, sport=sport)
        data = (max(0, size - len(pkt))+i) * 'x'
        sendp(pkt/data, iface=devices[direction]['name'])
        iter = iter+1
        sleep(0.05)


def parse_pmd_stats_output(pmd_stats):
    """Get queues from pmd-rxq-show command

    Return output of command: ovs-appctl dpif-netdev/pmd-rxq-show

    :param pmd_stats: string with pmd stats
    :return list with queues
    """
    port_regex = "  port: ([a-zA-Z\\-0-9]+)\\s+queue-id:\\s+(\\d+) " \
                 "\\(enabled\\)\\s+pmd usage:\\s+(\\d+) %"
    queues = []
    for line in pmd_stats:
        port_out = re.search(port_regex, line)
        if port_out:
            queue = {}
            queue["port"] = port_out.group(1)
            queue["queue_id"] = int(port_out.group(2))
            queue["pmd_usage"] = int(port_out.group(3))
            queues.append(queue)

    return queues


def parse_pmd_stats(queues_json, pmd_stats, pps):
    """Include pmd stats to the queues json file

    Include pmd stats to the queues json file:
    - map queues to queues ids returned by pmd stats
    - include some pps/pmd_usage values

    It is expected a injection like this one:
    [{'1': 0.3, '0': 1.2, '2': 0.1}, {'1': 0.3, '0': 0.8, '2': 0.1}]
    - interface 0, queue 0: higher traffic --> map this physical queue
    with its virtual queue
    - Remaining physical queue and virtual queue will map together
    - for each interface each queue have a different rate, so it will
    be possible to get queue_id based on the cpu reported

    :param queues_json: json with queues parsed from testpmd.log
    :param pmd_stats: pmd stats string after a injection
    :param pps: injection parameter
    :return updated queues_json
    """

    for port in range(len(queues_json)):
        for queue in queues_json[port]["queues"].keys():
            queues_json[port]["queues"][queue]["hyp_queues"] = []
            queues_json[port]["queues"][queue]["rate"] = 0

    queues = parse_pmd_stats_output(pmd_stats)
    filt_queues = [d for d in queues if d['pmd_usage'] > 0]
    sorted_queues = sorted(filt_queues,
                           key=lambda d: d['pmd_usage'],
                           reverse=True)
    queue_names = []
    queue_names.append([[d["port"] for d in sorted_queues
                         if 'vhu' not in d["port"]][0],
                        [d["port"] for d in sorted_queues
                         if 'vhu' in d["port"]][0]])
    queue_names.append(list(set([d["port"] for d in sorted_queues
                                 if d["port"] not in queue_names[0]])))
    queue_ids_phy = []
    queue_ids_vhu = []
    queue_ids_phy.append([d for d in sorted_queues
                         if 'vhu' not in d["port"]
                          and d["port"] in queue_names[0]])
    queue_ids_phy.append([d for d in sorted_queues
                         if 'vhu' not in d["port"]
                          and d["port"] in queue_names[1]])
    queue_ids_vhu.append([d for d in sorted_queues
                         if 'vhu' in d["port"]
                          and d["port"] in queue_names[0]])
    queue_ids_vhu.append([d for d in sorted_queues
                         if 'vhu' in d["port"]
                          and d["port"] in queue_names[1]])
    for port_index, port_value in enumerate(queue_ids_phy):
        for queue_id in range(int(len(port_value))):
            queue = queues_json[port_index]["queues"][str(queue_id)]
            queue["hyp_queues"].\
                append(queue_ids_phy[port_index][queue_id])
            queue["hyp_queues"].\
                append(queue_ids_vhu[port_index][queue_id])
            queue["rate"] = pps[port_index][str(queue_id)]

    return queues_json


def parse_testpmd_log(devices, file, start_seq):
    """Parse testpmd log file

    Parse testpmd log file and extract which queue received each
    ip address

    param devices: devices in which packets were sent
    param file: testpmd log file
    param start_seq: start seq number for packet generation
    return output: for each port and queue, list of ips received
    """
    output = []
    for interface in range(len(devices)):
        output_item = {'name': devices[interface]['name'], 'queues': {}}
        output.append(output_item)
        src_mac = devices[interface]['src_mac']
        ip_start = str(ipaddress.IPv4Address('48.0.0.1') + start_seq)
        with open(file, 'r') as tp:
            for ln in tp:
                log_src_mac = re.search('src='+src_mac.upper(), ln)
                log_queue_id = re.search('(Receive queue|RSS queue)=0x\\d+',
                                         ln)
                log_sw_ptype = re.search('sw ptype: L2_ETHER L3_IPV4 L4_UDP ',
                                         ln)
                if log_src_mac and log_queue_id and log_sw_ptype:
                    queue = int(log_queue_id.group().split('=')[1], 16)
                    len_parsed = int(re.search('length=\\d+', ln).
                                     group().split('=')[1])
                    value = ipaddress.IPv4Address(ip_start) + (len_parsed - 65)
                    if queue not in output_item['queues']:
                        output_item['queues'][queue] = {"pps": 0.2,
                                                        "isg": 0,
                                                        "ips": []}
                    output_item['queues'][queue]["ips"] += [str(value)]

    return(output)


class STLImix(object):

    def create_stream(self, pps, vm, src_mac, dst_mac, src_ip, dst_ip,
                      src_port, dst_port, isg=0, multiplier=1):
        """Create a stream

        Create a trex stream

        param pps: packets per second in mpps
        param vm: changing parameter in the flow
        param src_mac: source mac address
        param dst_mac: destination mac address
        param src_ip: source ip address
        param dst_ip: destination ip address
        param src_port: source port
        param dst_port: destination port
        param isg: stream delay
        param multiplier: multiply to pps
        return stream: stream generated
        """
        size = 64
        base_pkt = Ether(src=src_mac,
                         dst=dst_mac)/IP(src=src_ip,
                                         dst=dst_ip)/UDP(dport=dst_port,
                                                         sport=src_port)
        pad = max(0, size - len(base_pkt)) * 'x'
        pkt = STLPktBuilder(pkt=base_pkt/pad,
                            vm=vm)

        return STLStream(isg=isg,
                         packet=pkt,
                         mode=STLTXCont(pps=pps*1000000*float(multiplier)))

    def get_streams(self, src_mac, dst_mac, src_ip, dst_ip, src_port, dst_port,
                    flowvar, qratio, multiplier, **kwargs):
        """Generate a list of streams

        Generate a list of streams

        param src_mac: source mac address
        param dst_mac: destination mac address
        param src_ip: source ip address
        param dst_ip: destination ip address
        param src_port: source port
        param dst_port: destination port
        param flowvar: changing flow parameter
        param qratio: for each queue, pps and ips are included
        param multiplier: multiply to pps
        return streams: List of streams
        """
        streams = []
        for queue in qratio.keys():
            if qratio[queue]["pps"] > 0:
                vm = STLScVmRaw([
                    STLVmFlowVar(name=flowvar[0],
                                 value_list=qratio[queue]["ips"],
                                 op="inc"),
                    STLVmWrFlowVar(fv_name=flowvar[0],
                                   pkt_offset=flowvar[1]),
                    STLVmFixIpv4(offset='IP'),
                    STLVmFixChecksumHw(l3_offset="IP",
                                       l4_offset="UDP",
                                       l4_type=CTRexVmInsFixHwCs.L4_TYPE_UDP)])
                streams.append(self.create_stream(float(qratio[queue]["pps"]),
                                                  vm, src_mac, dst_mac, src_ip,
                                                  dst_ip, src_port, dst_port,
                                                  multiplier))
        return streams


def gen_stl(devices, traffic, duration, multiplier):
    """Generate traffic with trex

    Connect to trex, generate streams and start injecting traffic

    param devices: nics in which traffic will be generated
    param traffic: json with information about ports and streams
    param duration: injection duration in seconds
    param multiplier: multiply to each pps to increase rate
    """
    c = STLClient(verbose_level="error")

    def signal_handler(sig, frame):
        c.stop(ports=my_ports)
        c.disconnect()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    passed = True
    try:
        c.connect()
        my_ports = [0, 1]
        c.reset(ports=my_ports)
        c.remove_all_streams(my_ports)
        ports_used = []
        traffic_ips = ["16.0.0.1", "48.0.0.1"]
        traffic_ports = [1025, 32768]
        flow_var = [["dst_ip", 'IP.dst'], ['IP.src', 'IP.src']]
        for port in my_ports:
            streams = STLImix().get_streams(devices[port]['src_mac'],
                                            devices[port]['dest_mac'],
                                            traffic_ips[(port+2) % 2],
                                            traffic_ips[(port+1) % 2],
                                            traffic_ports[(port+2) % 2],
                                            traffic_ports[(port+1) % 2],
                                            flow_var[(port+2) % 2],
                                            traffic[port]['queues'],
                                            multiplier)
            if len(streams) > 0:
                c.add_streams(streams, ports=[port])
                ports_used.append(port)
        my_ports = ports_used
        c.start(ports=my_ports, mult="1", duration=duration)
        c.wait_on_traffic(ports=my_ports)
    except STLError as e:
        passed = False
        print(e)
    finally:
        c.disconnect()


class RawFormatter(argparse.HelpFormatter):
    def _fill_text(self, text, width, indent):
        return "\n".join([textwrap.fill(line, width) for line in
                          textwrap.indent(textwrap.dedent(text),
                                          indent).splitlines()])


def main():
    description = '''
Multiqueue traffic generator
Based on this other script:
https://github.com/yogananth-subramanian/multiqueue_traffic_gen/blob/0bfa30bf4dbe9d10a5539798ae7505168f3adebd/mq.py

It has 3 main functions:
* learning: Using scapy it generates several packets with different source or
  destination ip address. Each packet will have different size too so that it
  can be recognized either by the ip or the packet size. In testpmd it is
  possible to log each packet received in each queue, but it is not printed
  out the ip, so using a map between ip and packet size it is possible to know
  which ip is being received in that queue

* parse_testpmd: parse testpmd log. It gets which queue received each packet

* parse_pmd_stats: parse pmd log. It maps queue ids from pmd stats command to
  the queue ids got from testpmd.log
  In order to map queues ids, the following is required:
  1. queue ids "0" will have the higher rate for both ports
  2. queue id "0" will be higher in port 0 than in port 1
  3. rate for the following ports will decrease
  Example:
  port 0:
     queue 0, rate 1.2
     queue 1, rate 0.5
     queue 2, rate 0.1
  port 1:
     queue 0, rate 0.8
     queue 1, rate 0.5
     queue 2, rate 0.1

* gen_traffic: generate traffic using trex, it is possible to send traffic to
  specific queues

Examples on how to use it:
* learning:
  multiqueue.py  --action learning --packets 0 40
  It will generate packets from 48.0.0.1 to 48.0.0.40. It will generate traffic
  in both interfaces, in one interface this will be source ip while in te other
  it will be destination ip

* parse_testpmd:
  multiqueue.py --action parse_testpmd --packets 0 40 --log /tmp/testpmd.log
                --traffic_json /tmp/queues.json
  It will parse testpmd log and generate queues.json file with a list of ip
  address received by each port and queue.

* parse_stats_file:
  multiqueue.py  --action parse_pmd_stats --traffic_json /tmp/queues.json
        --pmd_stats_file /tmp/output
        --pps "[{'0': 1.2, '1': 0.5,'2':0.1},{'0':0.8,'1': 0.5,'2':0.1} ]"
  Parses file generated with command "ovs-appctl dpif-netdev/pmd-rxq-show"
  after injecting traffic

* gen_traffic:
  multiqueue.py --traffic_json /tmp/queues.json --duration 60 --multiplier 1 \
                --pps "[{{"0": 0.5}},{{"1": 0.8}}]"
  Using trex it will inject traffic to the specific queues. In this case, it
  will inject 0.5 mpps to port 0 queue 0 and 0.8 mpps to port 1 queue 1.
  Ports, queues and flows to used are defined in queues.json file. Injection
  duration will be 60 seconds. With multiplier parameter it can inject at
  higher rates, for example, if multiplier would have been 10, injections
  would be at 5 and 8 mpps.
'''
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=RawFormatter)

    parser.add_argument("--action", required=True,
                        choices=['learning', 'parse_testpmd',
                                 'parse_pmd_stats', 'gen_traffic'],
                        action='store')
    parser.add_argument("--packets", nargs='*', type=int, action='store')
    parser.add_argument('--traffic_json', action='store')
    parser.add_argument('--log', action='store')
    parser.add_argument('--pmd_stats_file', action='store')
    parser.add_argument('--duration', type=int, action='store')
    parser.add_argument('--multiplier', type=int, action='store')
    parser.add_argument('--pps', action='store')
    args = parser.parse_args()

    devices = trex_cfg()

    if args.action == "parse_testpmd":
        with open(args.traffic_json, 'w') as f:
            json.dump(parse_testpmd_log(devices,
                                        args.log,
                                        args.packets[0]), f, indent=4)
    elif args.action == "parse_pmd_stats":
        with open(args.traffic_json, 'r') as f:
            queues_json = json.load(f)
        with open(args.pmd_stats_file) as f:
            pmd_stats = f.readlines()
        with open(args.traffic_json, 'w') as f:
            json.dump(parse_pmd_stats(queues_json,
                                      pmd_stats,
                                      ast.literal_eval(args.pps)),
                      f,
                      indent=4)
    elif args.action == "learning":
        gen_scapy_pkt(devices, args.packets[1],
                      'UDP', start_seq=args.packets[0])
        gen_scapy_pkt(devices, args.packets[1],
                      'UDP', start_seq=args.packets[0], direction=1)
    elif args.action == "gen_traffic":
        with open(args.traffic_json, 'r') as f:
            traffic = json.load(f)

        if args.pps:
            pps = ast.literal_eval(args.pps)
            for port in range(len(traffic)):
                for key, value in traffic[port]['queues'].items():
                    if key in pps[port].keys():
                        value['pps'] = pps[port][key]
                    else:
                        value['pps'] = 0

        print(traffic)
        gen_stl(devices, traffic, args.duration, args.multiplier)

if __name__ == '__main__':
    main()
