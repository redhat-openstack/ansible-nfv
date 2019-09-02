#!/bin/env python
# Copyright 2018 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# The script configures instance with one or multiple network interfaces.
# It relies on the cloud-init package that perform the proper network
# configuration on the first boot.
#
# For the proper execution, the location of the script should be:
# "/var/lib/cloud/scripts/per-boot/", which will cause it to run every boot.
#
# During the first boot, the script dumps network configuration and stores it
# locally. During the next boot, the script takes the network dump and applies
# it on the system based on the changed (if changed) network interfaces.
#
# The script set SSH configuration to "UseDNS=no" to prevent login delay.
#
# The script updates the default route for the proper interface with the
# minimum metric value based on the provided "tag" by the user. The "tag"
# should be tied to the interface that the default route should be set with.
#
# HOW-TO-USE! - To use the script alongside with the openstack_tasks role,
# convert it to the base64 format and provide as the user data under the write
# files.

import argparse
import json
import logging
import os
import subprocess
import sys
import re

logging.basicConfig(filename='/var/log/messages', filemode='a',
                    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                    datefmt="%h %d %H:%M:%S", level=logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger = logging.getLogger("CustomNetConfig")
logger.addHandler(handler)


parser = argparse.ArgumentParser(
    description='Multi-interface network config script')
parser.add_argument('-i', '--init', help='Force creation of the network '
                                         'config dump')
parser.add_argument('-t', '--tag', help='The tag assignment is used for '
                                        'the default gateway '
                                        'configuration. The tag assigned '
                                        'to port, gets highest metric '
                                        'priority',
                    default="external")
parser.add_argument('--nics_data_path', help='Location of the json data '
                                             'file to store nics '
                                             'configuration',
                    default='/var/lib/cloud/data/nics_conf.json')
args = parser.parse_args()


def cloud_init_installed():
    """Verify cloud-init installed"""
    if os.path.exists('/etc/cloud/cloud.cfg'):
        return True
    return False


def configure_ssh_dns():
    """Set SSH to not query for DNS resolve. Solve delay during login."""
    with open('/etc/ssh/sshd_config', 'r+') as f:
        ssh_config = f.read()
        if re.search(r'UseDNS=no', ssh_config):
            logger.info('The SSH "UseDNS=no" configuration found.')
        else:
            f.write('\nUseDNS=no')
            logger.info('Write "UseDNS=no" to SSH config')
            os.system('systemctl restart sshd')


def check_existing_interfaces():
    """Check and locate existing network interfaces on instance"""
    ifaces = []
    nics = os.listdir('/sys/class/net/')
    nics.remove('lo')
    for nic in nics:
        nic_path = '/sys/class/net/{}/address'.format(nic)
        with open(nic_path, 'r') as f:
            mac = f.read().rstrip()
        ifaces.append({nic: mac})
    return ifaces


def dump_interfaces_config(nics=None):
    """Dump ifcfg files data"""
    if not nics:
        msg = 'The "nics" dict should hold ifaces macs. Currently empty.'
        logger.info(msg)
        raise ValueError(msg)

    iface_dump = []
    iface_content = {}
    data_path = args.nics_data_path
    for nic in nics:
        for key, value in iter(nic.items()):
            ifcfg_path = '/etc/sysconfig/network-scripts/ifcfg-{}'.format(key)
            if os.path.exists(ifcfg_path):
                logger.info('The {} interface found'.format(key))
                try:
                    with open(ifcfg_path, 'r') as iface_file:
                        iface_dump = iface_file.readlines()
                        logger.info('Read {} file content'.format(ifcfg_path))
                except IOError:
                    logger.info('Unable to read {} file.'.format(ifcfg_path))

                iface_content[value] = []
                for opt in iface_dump:
                    iface_content[value].append(opt)
            else:
                logger.info('The {} interface is missing'.format(key))
    try:
        with open(data_path, 'w') as jsonfile:
            json.dump(iface_content, jsonfile)
            logger.info('Write ifaces data to {}'.format(data_path))
    except IOError:
        logger.info('Unable to write data to {} file'.format(data_path))
    logger.info('Network data has been successfully dumped')


def recreate_interfaces_config(dump_config_file, nics=None):
    """Recreate interfaces config based on the dumped data"""
    if not dump_config_file or not nics:
        msg = 'Missing one of the following: nics list or interfaces dump.'
        logger.info(msg)
        raise ValueError(msg)

    logger.info('Read interfaces dump file')
    with open(dump_config_file) as json_file:
        dump_config = json.load(json_file)

    for nic in nics:
        for nic_name, nic_mac in iter(nic.items()):
            for mac in dump_config:
                if nic_mac == mac:
                    ifcfg_path = '/etc/sysconfig/network-scripts/' \
                                 'ifcfg-{}'.format(nic_name)
                    for num, item in enumerate(dump_config[mac]):
                        if 'DEVICE' in item:
                            dump_config[mac][num] = 'DEVICE={}' \
                                                    '\n'.format(nic_name)
                    with open(ifcfg_path, 'w') as ifcfg_file:
                        ifcfg_file.writelines(dump_config[mac])
    os.system('systemctl restart network')
    logger.info('Network configuration has been completed')


def get_tag():
    """Check "tag" existence for the interface

    The "tag" that should be tied to the interface will be used to set the
    requested default route.
    """
    try:
        os.system('mount /dev/sr0 /mnt')
        logger.info('Config drive mounted')
        with open('/mnt/openstack/latest/meta_data.json') as json_file:
            metadata = json.load(json_file)
        os.system('umount /mnt')
        logger.info('Config drive unmounted')
    except ValueError:
        logger.info('Unable to mount config drive or fetch metadata.')

    metadata = metadata['devices']
    for meta in metadata:
        if 'tags' in meta:
            tags = meta['tags']
            for tag in tags:
                if args.tag == tag:
                    logger.info('The tag "{}" for mac "{}" found'.
                                format(tag, meta['mac']))
                    meta_data = {'mac': meta['mac'], 'tag': tag}
                    return meta_data
            return None


def list_default_routes():
    """List default routes of the instance"""
    default_routes = []
    out = subprocess.Popen(['ip', 'route', 'show'], stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    routes = stdout.split(' \n')
    for route in routes:
        if 'default' in route:
            default_routes.append(route)
    return default_routes


def set_default_route(routes, tag, nics):
    """Set default route for instance based on tag

    The route replaced with the same route but contains lower metric.
    This is done to ensure that the requested route always will get priority.
    """
    old_route = None
    new_route = None
    for nic in nics:
        for nic_name, nic_mac in iter(nic.items()):
            if nic_mac == tag['mac'] and tag['tag'] == args.tag:
                old_route = [route for route in routes if nic_name in route]
                old_route = old_route[0].split()
                new_route = old_route[:-1]
                new_route.append('10')
    if old_route and new_route:
        del_route_cmd = ['ip', 'route', 'del']
        del_route_cmd.extend(old_route)
        logger.info('Remove route: "{}"'.format(' '.join(del_route_cmd)))
        del_route = subprocess.Popen(del_route_cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
        del_route.communicate()

        set_route_cmd = ['ip', 'route', 'add']
        set_route_cmd.extend(new_route)
        logger.info('Set route: "{}"'.format(' '.join(set_route_cmd)))
        set_route = subprocess.Popen(set_route_cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
        set_route.communicate()


def main():
    logger.info('Start network configuration')
    if not cloud_init_installed():
        raise ValueError('The instance must have cloud-init installed to'
                         'properly configure the networking.')
    configure_ssh_dns()
    ifaces = check_existing_interfaces()
    if args.init or not os.path.exists(args.nics_data_path):
        logger.info('Dump interfaces config')
        dump_interfaces_config(ifaces)
    else:
        logger.info('Recreate network configuration')
        recreate_interfaces_config(args.nics_data_path, ifaces)
    tag = get_tag()
    if tag:
        logger.info('Set default gateway')
        default_routes = list_default_routes()
        set_default_route(default_routes, tag, ifaces)
    logger.info('Network configuration completed')


if __name__ == '__main__':
    main()
