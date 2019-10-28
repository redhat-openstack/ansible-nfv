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

# The script keeps the consistent configuration of the network interfaces
# provided by the cloud-init over the reboots of the vm by the following steps:
#
# On first boot (dump file does not exist) or if the '--init' param is used:
#  * Dumps the configuration provided by the cloud-init
#  * The configuration placed into a json file within the instance
#  * If a "tag" provided within the port meta-data, use it to set the selected
#    interface as the default gateway with the lowest metric.
#  * The route metric value stored within the dump for the required interface.
#  * Set the SSH configuration to "UseDNS no" to prevent login delay.
# On the reboot
#  * After the reboot, the script restores the network configuration from the
#    dump stored previously including the route metric.
#
# For the proper execution, place the script within the location that will
# execute the script over each reboot:
# "/var/lib/cloud/scripts/per-boot/"

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
                    default='/var/lib/cloud/data/custom_net_config_dump.json')
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
        if re.search(r'UseDNS no', ssh_config):
            logger.info('The SSH "UseDNS no" configuration found.')
        else:
            f.write('\nUseDNS no')
            f.flush()
            logger.info('Write "UseDNS no" to SSH config')
            execute_shell_command('systemctl restart sshd')


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


def dump_interfaces_config(nics=None, tag=None):
    """Dumps ifcfg files data and route metric"""
    if not nics:
        msg = 'The "nics" dict should hold ifaces macs. Currently empty.'
        logger.info(msg)
        raise ValueError(msg)

    iface_dump = []
    iface_content = {}
    data_path = args.nics_data_path
    for nic in nics:
        for nic_name, nic_mac in iter(nic.items()):
            ifcfg_path = '/etc/sysconfig/network-scripts/' \
                         'ifcfg-{}'.format(nic_name)
            if os.path.exists(ifcfg_path):
                logger.info('The {} interface found'.format(nic_name))
                try:
                    with open(ifcfg_path, 'r') as iface_file:
                        iface_dump = iface_file.readlines()
                        logger.info('Read {} file content'.format(ifcfg_path))
                except IOError:
                    logger.info('Unable to read {} file.'.format(ifcfg_path))

                iface_content[nic_mac] = []
                for opt in iface_dump:
                    iface_content[nic_mac].append(opt)

                if tag and nic_mac == tag['mac'] and tag['tag'] == args.tag:
                    logger.info('Dump lower gateway metric for {} '
                                'interface'.format(nic_name))
                    iface_content[nic_mac].append('IPV4_ROUTE_METRIC=10\n')
            else:
                logger.info('The {} interface is missing'.format(nic_name))
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
    logger.info('Network interfaces has been restored.')


def get_tag():
    """Check "tag" existence for the interface

    The "tag" that should be tied to the port will be used to set the
    requested default route.
    """
    try:
        config_drive = execute_shell_command('mount /dev/sr0 /mnt')
        logger.info(config_drive)
        with open('/mnt/openstack/latest/meta_data.json') as json_file:
            metadata = json.load(json_file)
        execute_shell_command('umount /mnt')
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


def set_default_route(nics, tag):
    """Set default route for instance based on tag

    The route set to the ifcfg file with the lower metric.
    This is done to ensure that the requested route always will get priority.
    """
    for nic in nics:
        for nic_name, nic_mac in iter(nic.items()):
            if nic_mac == tag['mac'] and tag['tag'] == args.tag:
                ifcfg_path = '/etc/sysconfig/network-scripts/' \
                             'ifcfg-{}'.format(nic_name)
                with open(ifcfg_path, 'a') as ifcfg_file:
                    ifcfg_file.write('IPV4_ROUTE_METRIC=10')
                logger.info('The metric "10" has been set to {} '
                            'interface.'.format(nic_name))


def execute_shell_command(cmd):
    """Execute shell command

    The subprocess.check_output executes command provided as list.
    If the command will be provided as string, it will be converted to list
    and then executed.
    """
    if not isinstance(cmd, list):
        cmd = cmd.split()
    try:
        logger.info('Execute command: {}'.format(cmd))
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        logger.info('Command failed: {}'.format(e))
        raise
    return output


def main():
    logger.info('Start network configuration')
    if not cloud_init_installed():
        raise ValueError('The instance must have cloud-init installed to'
                         'properly configure the networking.')
    configure_ssh_dns()
    ifaces = check_existing_interfaces()
    if args.init or not os.path.exists(args.nics_data_path):
        logger.info('Check for port tag')
        tag = get_tag()
        logger.info('Dump interfaces config')
        dump_interfaces_config(ifaces, tag)
        if tag:
            set_default_route(ifaces, tag)
    else:
        logger.info('Recreate network configuration')
        recreate_interfaces_config(args.nics_data_path, ifaces)
    execute_shell_command('systemctl restart network')
    logger.info('Network configuration completed')


if __name__ == '__main__':
    main()
