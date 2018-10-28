#!/usr/bin/python
# _*_ coding: utf-8 _*_

#
# Dell EMC OpenManage Ansible Modules
# Version 1.0
# Copyright (C) 2018 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule
from omdrivers.enums.iDRAC.iDRAC import *
# from omsdk.sdkfile import FileOnShare
# import logging.config

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_configure_idrac_services
short_description: Configures the iDRAC services attributes.
version_added: "2.3"
description:
    - This module is responsible for configuring the iDRAC services attributes.
options:
    idrac_ip:
        required: True
        description: iDRAC IP Address
        default: None
    idrac_user:
        required: True
        description: iDRAC username
        default: None
    idrac_pwd:
        required: True
        description: iDRAC user password
        default: None
    idrac_port:
        required: False
        description: iDRAC port
        default: 443
    share_name:
        required: True
        description: Network share or a local path.
    share_user:
        required: False
        description: Network share user in the format 'user@domain' if user is part of a domain else 'user'
    share_pwd:
        required: False
        description: Network share user password
    share_mnt:
        required: False
        description: Local mount path of the network share with read-write permission for ansible user
    enable_web_server:
        required: False
        description: Whether to Enable or Disable webserver configuration for iDRAC
        choices: [Enabled, Disabled]
    ssl_encryption:
        required: False
        description: Secure Socket Layer encryption for webserver
        choices: [Auto_Negotiate, T_128_Bit_or_higher, T_168_Bit_or_higher, T_256_Bit_or_higher]
    tls_protocol:
        required: False
        description: Transport Layer Security for webserver
        choices: [TLS_1_0_and_Higher, TLS_1_1_and_Higher, TLS_1_2_Only]
    https_port:
        required: False
        description: HTTPS access port.
    http_port:
        required: False
        description: HTTP access port.
    timeout:
        required: False
        description: Timeout value.
    snmp_enable:
        required: False
        description: Whether to Enable or Disable SNMP protocol for iDRAC
        choices: [Enabled, Disabled]
    snmp_protocol:
        required: False
        description: Type of the SNMP protocol
        choices: [All, SNMPv3]
    community_name:
        required: False
        description: SNMP community name for iDRAC
        default: None
    alert_port:
        required: False
        description: SNMP alert port for iDRAC
        default: None
    discovery_port:
        required: False
        description: SNMP discovery port for iDRAC.
        default: 162
    trap_format:
        required: False
        description: SNMP trap format for iDRAC
        default: None
requirements:
    - "omsdk"
    - "python >= 2.7"
author: "OpenManageAnsibleEval@dell.com"

"""

EXAMPLES = """
---
- name: Configure the iDRAC services attributes.
  dellemc_configure_idrac_services:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       share_name: "\\\\xx.xx.xx.xx\\share"
       share_pwd:  "xxxxxxxx"
       share_user: "xxxx"
       share_mnt: "/mnt/share"
       enable_web_server: "Enabled"
       http_port: "80"
       https_port: "443"
       ssl_encryption: "Auto_Negotiate"
       tls_protocol: "TLS_1_2_Only"
       timeout: "1800"
       snmp_enable: "Enabled"
       snmp_protocol: "SNMPv3"
       community_name: "None"
       alert_port: "None"
       discovery_port: "162"
       trap_format: "None"
"""

RETURNS = """
---
- dest:
    description: Configures the iDRAC services attributes.
    returned: success
    type: string
"""

# log_root = '/var/log'
# dell_emc_log_path = log_root + '/dellemc'
# dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'
#
# logging.config.fileConfig(dell_emc_log_file,
#                           defaults={'logfilename': dell_emc_log_path + '/dellemc_idrac_services_config.log'})
# # create logger
# logger = logging.getLogger('ansible')


def run_idrac_services_config(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: iDRAC services configuration method')
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:

        idrac.use_redfish = True
        logger.info(module.params['idrac_ip'] + ': CALLING: File on share OMSDK API')
        upd_share = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                        mount_point=module.params['share_mnt'],
                                                        isFolder=True,
                                                        creds=UserCredentials(
                                                            module.params['share_user'],
                                                            module.params['share_pwd'])
                                                        )
        logger.info(module.params['idrac_ip'] + ': FINISHED: File on share OMSDK API')

        logger.info(module.params['idrac_ip'] + ': CALLING: Set liasion share OMSDK API')
        set_liason = idrac.config_mgr.set_liason_share(upd_share)
        if set_liason['Status'] == "Failed":
            try:
                message = set_liason['Data']['Message']
            except (IndexError, KeyError):
                message = set_liason['Message']
            err = True
            msg['msg'] = "{}".format(message)
            msg['failed'] = True
            logger.info(module.params['idrac_ip'] + ': FINISHED: {}'.format(message))
            return msg, err

        logger.info(module.params['idrac_ip'] + ': FINISHED: Set liasion share OMSDK API')

        logger.info(module.params['idrac_ip'] + ': CALLING: Setup iDRAC Webserver Configuration')

        if module.params['enable_web_server'] != None:
            idrac.config_mgr.configure_web_server(
                enable_web_server=Enable_WebServerTypes[module.params['enable_web_server']]
            )
        if module.params['http_port'] != None:
            idrac.config_mgr.configure_web_server(
                http_port=module.params['http_port']
            )
        if module.params['https_port'] != None:
            idrac.config_mgr.configure_web_server(
                https_port=module.params['https_port']
            )
        if module.params['timeout'] != None:
            idrac.config_mgr.configure_web_server(
                timeout=module.params['timeout']
            )
        if module.params['ssl_encryption'] != None:
            idrac.config_mgr.configure_web_server(
                ssl_encryption=SSLEncryptionBitLength_WebServerTypes[module.params['ssl_encryption']]
            )
        if module.params['tls_protocol'] != None:
            idrac.config_mgr.configure_web_server(
                tls_protocol=TLSProtocol_WebServerTypes[module.params['tls_protocol']]
            )
        logger.info(module.params['idrac_ip'] + ': FINISHED: Setup iDRAC Webserver Configuration')

        logger.info(module.params['idrac_ip'] + ': CALLING: Setup SNMP for iDRAC')
        if module.params['snmp_enable'] != None:
            idrac.config_mgr.configure_snmp(
                snmp_enable=AgentEnable_SNMPTypes[module.params['snmp_enable']]
            )
        if module.params['community_name'] != None:
            idrac.config_mgr.configure_snmp(
                community_name=module.params['community_name']
            )
        if module.params['snmp_protocol'] != None:
            idrac.config_mgr.configure_snmp(
                snmp_protocol=SNMPProtocol_SNMPTypes[module.params['snmp_protocol']]
            )
        if module.params['alert_port'] != None:
            idrac.config_mgr.configure_snmp(
                alert_port=module.params['alert_port']
            )
        if module.params['discovery_port'] != None:
            idrac.config_mgr.configure_snmp(
                discovery_port=module.params['discovery_port']
            )
        if module.params['trap_format'] != None:
            idrac.config_mgr.configure_snmp(
                trap_format=module.params['trap_format']
            )
        logger.info(module.params['idrac_ip'] + ': FINISHED: Setup SNMP for iDRAC')

        msg['msg'] = idrac.config_mgr.apply_changes(reboot=False)

        if "Status" in msg['msg']:
            if msg['msg']['Status'] == "Success":
                msg['changed'] = True
                if "Message" in msg['msg']:
                    if msg['msg']['Message'] == "No changes found to commit!":
                        msg['changed'] = False
            else:
                msg['failed'] = True
    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: iDRAC services configuration method')
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC services configuration method')
    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC Handle
            idrac=dict(required=False, type='dict'),

            # iDRAC credentials
            idrac_ip=dict(required=True, default=None, type='str'),
            idrac_user=dict(required=True, default=None, type='str'),
            idrac_pwd=dict(required=True, default=None,
                           type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Export Destination
            share_name=dict(required=True, type='str'),
            share_pwd=dict(required=False, type='str', no_log=True),
            share_user=dict(required=False, type='str'),
            share_mnt=dict(required=False, type='str'),

            # setup Webserver
            enable_web_server=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            http_port=dict(required=False, default=None, type='int'),
            https_port=dict(required=False, default=None, type='int'),
            ssl_encryption=dict(required=False, choices=['Auto_Negotiate', 'T_128_Bit_or_higher',
                                                         'T_168_Bit_or_higher', 'T_256_Bit_or_higher'],
                                default=None),
            tls_protocol=dict(required=False, choices=['TLS_1_0_and_Higher',
                                                       'TLS_1_1_and_Higher', 'TLS_1_2_Only'], default=None),
            timeout=dict(required=False, default=None, type="str"),

            # set up SNMP
            snmp_enable=dict(required=False, choices=['Enabled', 'Disabled'], default=None),
            community_name=dict(required=False, type='str', default=None),
            snmp_protocol=dict(required=False, choices=['All', 'SNMPv3'], default=None),
            alert_port=dict(required=False, default=None),
            discovery_port=dict(required=False, default=None, type="int"),
            trap_format=dict(required=False, default=None),

        ),

        supports_check_mode=True)
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Server Configuration')
    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful')
    # Export Server Configuration Profile
    msg, err = run_idrac_services_config(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Server Configuration')


if __name__ == '__main__':
    main()
