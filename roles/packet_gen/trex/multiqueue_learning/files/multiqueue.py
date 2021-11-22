#!/usr/bin/python3
import sys
import sys
import os
import ipaddress
import json
import time
import argparse
import os
import yaml
import re
import pprint
import socket
from time import sleep
sys.path.append('/opt/trex/current/automation/trex_control_plane/server/')
import outer_packages  # noqa: E402
from trex.stl.api import *  # noqa: E402


def get_nics_from_macs():
    nic_output = {}
    nics = socket.if_nameindex()
    nics = [list(nic)[1] for nic in nics]
    for nic in nics:
        with open('/sys/class/net/{}/address'.format(nic), 'r') as f:
            nic_output[f.read().rstrip('\r\n')] = nic
    return nic_output


def trex_cfg():
    try:
        stream = open('/etc/trex_cfg.yaml', 'r')
        cfg_dict = yaml.safe_load(stream)
    except Exception as e:
        print(e)
        raise e

    nics = get_nics_from_macs()

    devices = []
    for i in range(len(cfg_dict[0]['port_info'])):
        device = {}
        src_mac = cfg_dict[0]['port_info'][i]['src_mac']
        dst_mac = cfg_dict[0]['port_info'][i]['dest_mac']
        if src_mac in nics.keys():
            device['name'] = nics[src_mac]
        device['dest_mac'] = dst_mac
        device['src_mac'] = src_mac
        devices.append(device)
    return devices


def gen_scapy_pkt(devices, maxpps, proto, start_seq=0,
                  src_port=1025, dst_port=32768, direction=0):
    ip_start = str(ipaddress.IPv4Address('48.0.0.1')+start_seq)
    size = 65
    end_seq = maxpps if maxpps-start_seq <= 1000 else 1000
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


def parse_testpmd_log(devices, file, start, end):
    output = []
    for interface in range(len(devices)):
        output_item = {'name': devices[interface]['name'], 'queues': {}}
        output.append(output_item)
        src_mac = devices[interface]['src_mac']
        ip_start = str(ipaddress.IPv4Address('48.0.0.1') + start)
        with open(file, 'r') as tp:
            for ln in tp:
                x = re.search('src='+src_mac.upper(), ln)
                y = re.search('(Receive queue|RSS queue)=0x\d+', ln)
                z = re.search('sw ptype: L2_ETHER L3_IPV4 L4_UDP ', ln)
                if x and y and z:
                    queue = int(y.group().split('=')[1], 16)
                    len_parsed = int(re.search('length=\d+', ln).
                                     group().split('=')[1])
                    value = ipaddress.IPv4Address(ip_start) + (len_parsed - 65)
                    if queue not in output_item['queues']:
                        output_item['queues'][queue] = {"pps": 0.2,
                                                        "isg": 0,
                                                        "ips": []}
                    output_item['queues'][queue]["ips"] += [str(value)]

    return(output)


class STLImix(object):

    def create_stream(self, pps, vm, src_mac, dst_mac, isg=0, multiplier=1):
        size = 64
        base_pkt = Ether(src=src_mac,
                         dst=dst_mac)/IP(src="16.0.0.1",
                                         dst="48.0.0.1")/UDP(dport=32768,
                                                             sport=1025)
        pad = max(0, size - len(base_pkt)) * 'x'
        pkt = STLPktBuilder(pkt=base_pkt/pad,
                            vm=vm)

        return STLStream(isg=isg,
                         packet=pkt,
                         mode=STLTXCont(pps=pps*1000000*float(multiplier)))

    def get_streams(self, src_mac, dst_mac, qratio, multiplier, **kwargs):
        streams = []
        for queue in qratio.keys():
            if qratio[queue]["pps"] > 0:
                vm = STLScVmRaw([
                    STLVmFlowVar(name="dst_ip",
                                 value_list=qratio[queue]["ips"],
                                 op="inc"),
                    STLVmWrFlowVar(fv_name='dst_ip',
                                   pkt_offset='IP.dst'),
                    STLVmFixIpv4(offset='IP'),
                    STLVmFixChecksumHw(l3_offset="IP",
                                       l4_offset="UDP",
                                       l4_type=CTRexVmInsFixHwCs.L4_TYPE_UDP)])
                streams.append(self.create_stream(float(qratio[queue]["pps"]),
                                                  vm,
                                                  src_mac,
                                                  dst_mac,
                                                  multiplier))
        return streams


def register():
    return STLImix()


def gen_stl(devices, traffic, duration, multiplier):
    c = STLClient(verbose_level="error")
    passed = True
    try:
        c.connect()
        my_ports = [0, 1]
        c.reset(ports=my_ports)
        c.remove_all_streams(my_ports)
        for port in my_ports:
            c.add_streams(register().get_streams(devices[port]['src_mac'],
                                                 devices[port]['dest_mac'],
                                                 traffic[port]['queues'],
                                                 multiplier), ports=[port])
        c.start(ports=my_ports, mult="1", duration=duration)
        c.wait_on_traffic(ports=my_ports)
    except STLError as e:
        passed = False
        print(e)
    finally:
        c.disconnect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", required=True,
                        choices=['learning', 'parse', 'gen_traffic'],
                        action='store')
    parser.add_argument("--packets", nargs='*', type=int, action='store')
    parser.add_argument('--traffic_json', action='store')
    parser.add_argument('--log', action='store')
    parser.add_argument('--duration', type=int, action='store')
    parser.add_argument('--multiplier', type=int, action='store')
    args = parser.parse_args()

    devices = trex_cfg()

    if args.action == "parse":
        with open(args.traffic_json, 'w') as f:
            json.dump(parse_testpmd_log(devices,
                                        args.log,
                                        args.packets[0],
                                        args.packets[1]), f, indent=4)
    elif args.action == "learning":
        gen_scapy_pkt(devices, args.packets[1],
                      'UDP', start_seq=args.packets[0])
        gen_scapy_pkt(devices, args.packets[1],
                      'UDP', start_seq=args.packets[0], direction=1)
    elif args.action == "gen_traffic":
        with open(args.traffic_json, 'r') as f:
            traffic = json.load(f)
        gen_stl(devices, traffic, args.duration, args.multiplier)
