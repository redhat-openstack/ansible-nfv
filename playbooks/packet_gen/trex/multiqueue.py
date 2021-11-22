#!/usr/bin/python3
import sys
import os
import ipaddress
import json
import time
import argparse
import os
import sys
import yaml
import re
import pprint
import socket
from time import sleep
sys.path.append('/opt/trex/current/automation/trex_control_plane/server/')
import outer_packages
from trex.stl.api import *


def get_nics_from_macs():
    nic_output={}
    nics=socket.if_nameindex()
    nics=[list(nic)[1] for nic in nics]
    for nic in nics:
        with open('/sys/class/net/{}/address'.format(nic), 'r') as f:
             nic_output[f.read().rstrip('\r\n')] = nic
    return nic_output

def trex_cfg():
    try:
        stream = open('/etc/trex_cfg.yaml', 'r')
        cfg_dict= yaml.safe_load(stream)
    except Exception as e:
        print(e);
        raise e

    nics = get_nics_from_macs()

    devices=[]
    for i in range(len(cfg_dict[0]['port_info'])):
        src_mac = cfg_dict[0]['port_info'][i]['src_mac']
        dst_mac = cfg_dict[0]['port_info'][i]['dest_mac']
        devices.append({'name': nics[src_mac] })
        devices[i]['dest_mac']= dst_mac
        devices[i]['src_mac']= src_mac
    return devices

def gen_scapy_pkt(devices, maxpps, proto, start_seq=0, src_port=1025, dst_port=32768, direction=0):
    ip_start =str(ipaddress.IPv4Address('48.0.0.1')+start_seq)
    size = 65
    end_seq = maxpps if maxpps-start_seq <= 1000 else 1000
    iter=0
    for i in range(start_seq, end_seq):
        print(str(ipaddress.IPv4Address(ip_start)+iter))
        pkt2 = Ether(src=devices[direction]['src_mac'],dst=devices[direction]['dest_mac'])
        pkt1 = pkt2/IP(dst=str(ipaddress.IPv4Address(ip_start)+iter),src="16.0.0.1")
        dport = dst_port
        sport = src_port
        if direction == 1:
            pkt1 = pkt2/IP(src=str(ipaddress.IPv4Address(ip_start)+iter),dst="16.0.0.1")
            dport = src_port
            sport = dst_port
        if proto == 'UDP':
            pkt = pkt1/UDP(dport=dport,sport=sport)
        else:
            pkt = pkt1/TCP(dport=dport,sport=sport)
        data = (max(0, size - len(pkt))+i) * 'x'
        sendp(pkt/data, iface=devices[direction]['name'])
        iter=iter+1
        sleep(0.05)

def parse_testpmd_log(devices, file, start, end):
    output = {}
    for interface in devices:
        output_item = {}
        output[interface['name']] = output_item
        src_mac = interface['src_mac']
        ips_limits = [ipaddress.IPv4Address('48.0.0.1') + start,
                      ipaddress.IPv4Address('48.0.0.1') + start + end]
        ip_start = str(ips_limits[0])
        with open(file, 'r') as tp:
            for ln in tp:
                x = re.search('src='+src_mac.upper(), ln)
                if x:
                    y = re.search('(Receive queue|RSS queue)=0x\d+', ln)
                    if y:
                        queue = int(y.group().split('=')[1], 16)
                        value = ipaddress.IPv4Address(ip_start)+(int(re.search('length=\d+', ln).group().split('=')[1])-65)
                        if int(value) in range(int(ips_limits[0]), int(ips_limits[1])):
                            output_item[queue] = output_item.get(queue, []) + [str(value)]
    return(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--packets", nargs='*', type=int, action='store')
    parser.add_argument('--parse', action='store')
    parser.add_argument('--log', action='store')
    args = parser.parse_args()

    devices=trex_cfg()

    if args.parse:
        with open(args.parse, 'w') as f:
           json.dump(parse_testpmd_log(devices, args.log, args.packets[0], args.packets[1]), f, indent=4)
    else:
        gen_scapy_pkt(devices, args.packets[1], 'UDP', start_seq=args.packets[0])
        gen_scapy_pkt(devices, args.packets[1], 'UDP', start_seq=args.packets[0], direction=1)
