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
from ansible.module_utils.basic import AnsibleModule
from omsdk.sdkfile import FileOnShare, file_share_manager
from omsdk.sdkcreds import UserCredentials
from omdrivers.enums.iDRAC.iDRACEnums import *
# import logging.config

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_import_server_config_profile
short_description: Import SCP from a network share or from a local file
version_added: "2.3"
description:
    - Import a given Server Configuration Profile (SCP) file from a network share or from a local file.
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
        description: Network share user in the format 'user@domain' if user is part of a domain else 'user'.
    share_pwd:
        required: False
        description: Network share user password
    scp_file:
        required: True
        description: Server Configuration Profile file name 
        default: None
    scp_components:
        required: False
        description:
            - if ALL,    this module will import all components configurations from SCP file
            - if IDRAC,  this module will import iDRAC configuration from SCP file
            - if BIOS,   this module will import BIOS configuration from SCP file
            - if NIC,    this module will import NIC configuration from SCP file
            - if RAID,   this module will import RAID configuration from SCP file
        choices: ['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID']
        default: 'ALL'

    shutdown_type:
        required: False
        description:
            - if Graceful, it gracefully shuts down the server.
            - if Forced,  it forcefully shuts down the server.
            - if NoReboot, it does not reboot the server.
        choices: ['Graceful', 'Forced', 'NoReboot']
        default: 'Graceful'

    end_host_power_state:
        required: False
        description:
            - if On, End host power state is on.
            - if Off, End host power state is off.
        choices: ['On' ,'Off']
        default: 'On'

    job_wait:
        required:  True
        description: Whether to wait for job completion or not
        choices: [True,  False] 

requirements:
    - "omsdk"
    - "python >= 2.7"
author: "OpenManageAnsibleEval@dell.com"

"""

EXAMPLES = """
---
- name: Import Server Configuration Profile
  dellemc_import_server_config_profile:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       share_name: "\\\\xx.xx.xx.xx\\share"
       share_user: "xxxx"
       share_pwd:  "xxxxxxxx"
       scp_file:   "scp_file.xml"
       scp_components: "ALL"
       job_wait: True
"""

RETURNS = """
---
- dest:
    description: Imports SCP from a network share or from a local file.
    returned: success
    type: string

"""

# log_root = '/var/log'
# dell_emc_log_path = log_root + '/dellemc'
# dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'
#
# logging.config.fileConfig(dell_emc_log_file, defaults={'logfilename': dell_emc_log_path + '/dellemc_import_scp.log'})
# # create logger
# logger = logging.getLogger('ansible')


def run_import_server_config_profile(idrac, module):
    """
    Import Server Configuration Profile from a network share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: Importing Server Configuration Profile Method')
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    msg['msg'] = {}
    err = False

    try:
        if module.check_mode:
            msg['changed'] = True

        else:

            logger.info(module.params['idrac_ip'] + ': CALLING: Create File share object OMSDK API')
            myshare = file_share_manager.create_share_obj(
                share_path=module.params['share_name'] + "/" + module.params['scp_file'],
                creds=UserCredentials(module.params['share_user'],
                                      module.params['share_pwd']), isFolder=False, )
            logger.info(module.params['idrac_ip'] + ': FINISHED: Create File share object OMSDK API')
            # myshare.new_file(module.params['scp_file'])

            scp_components = SCPTargetEnum.ALL

            if module.params['scp_components'] == 'IDRAC':
                scp_components = SCPTargetEnum.IDRAC
            elif module.params['scp_components'] == 'BIOS':
                scp_components = SCPTargetEnum.BIOS
            elif module.params['scp_components'] == 'NIC':
                scp_components = SCPTargetEnum.NIC
            elif module.params['scp_components'] == 'RAID':
                scp_components = SCPTargetEnum.RAID
            job_wait = module.params['job_wait']

            end_host_power_state = EndHostPowerStateEnum.On
            if module.params['end_host_power_state'] == 'Off':
                end_host_power_state = EndHostPowerStateEnum.Off

            shutdown_type = ShutdownTypeEnum.Graceful
            if module.params['shutdown_type'] == 'Forced':
                shutdown_type = ShutdownTypeEnum.Forced
            elif module.params['shutdown_type'] == 'NoReboot':
                shutdown_type = ShutdownTypeEnum.NoReboot

            logger.info(module.params['idrac_ip'] + ': STARTING: Importing Server Configuration Profile Method:'
                                                    ' Invoking OMSDK Import SCP API')
            idrac.use_redfish = True
            msg['msg'] = idrac.config_mgr.scp_import(myshare,
                                                     target=scp_components, shutdown_type=shutdown_type,
                                                     end_host_power_state=end_host_power_state,
                                                     job_wait=job_wait)
            logger.info(module.params['idrac_ip'] + ': FINISHED: Importing Server Configuration Profile Method:'
                                                    ' Invoked OMSDK Import SCP API')
            if "Status" in msg['msg']:
                if msg['msg']['Status'] == "Success":
                    if module.params['job_wait'] == True:
                        msg['changed'] = True
                        if "Message" in msg['msg']:
                            if "No changes were applied" in msg['msg']['Message']:
                                msg['changed'] = False
                else:
                    msg['failed'] = True

    except Exception as e:
        logger.error(
            module.params['idrac_ip'] + ': EXCEPTION: Importing Server Configuration Profile Method: ' + str(e))
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
    logger.info(module.params['idrac_ip'] + ': FINISHED: Imported Server Configuration Profile Method')
    return msg, err


# Main
def main():
    from ansible.module_utils.dellemc_idrac import iDRACConnection

    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC handle
            idrac=dict(required=False, type='dict'),

            # iDRAC Credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Network File Share
            share_name=dict(required=True, type='str'),
            share_user=dict(required=False, type='str'),
            share_pwd=dict(required=False, type='str', no_log=True),
            scp_file=dict(required=True, type='str'),
            scp_components=dict(required=False,
                                choices=['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID'],
                                default='ALL'),
            shutdown_type=dict(required=False,
                               choices=['Graceful', 'Forced', 'NoReboot'],
                               default='Graceful'),
            end_host_power_state=dict(required=False,
                                      choices=['On', 'Off'],
                                      default='On'),
            job_wait=dict(required=True, type='bool')
        ),

        supports_check_mode=True)
    logger.info(module.params['idrac_ip'] + ': STARTING: Import Server Configuration Profile')
    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()
    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful')
    msg, err = run_import_server_config_profile(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: Imported Server Configuration Profile')


if __name__ == '__main__':
    main()
