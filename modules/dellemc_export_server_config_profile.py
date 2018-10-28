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
# import logging.config

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_export_server_config_profile
short_description: Export Server Configuration Profile (SCP) to a network share or to a local file
version_added: "2.3"
description:
    - Export Server Configuration Profile
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
    scp_components:
        required: False
        description: Specify the hardware component(s) configuration to be exported
            - if ALL, the module will export all components configurations in SCP file
            - if IDRAC,  the module will export iDRAC configuration in SCP file
            - if BIOS,  the module will export BIOS configuration in SCP file
            - if NIC,  the module will export NIC configuration in SCP file
            - if RAID,  the module will export RAID configuration in SCP file
        choices: ['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID']
        default: 'ALL'
    job_wait:
        required:  True
        description: Whether to wait for job completion or not
        choices: [True,  False]
    export_format:
        required:  False
        description: Specify the output file format
        choices: ['JSON',  'XML']
        default: 'XML'
    export_use:
        required:  False
        description: Specify the type of server configuration profile (SCP) to be exported
        choices: ['Default',  'Clone', 'Replace']
        default: 'Default'

requirements:
    - "omsdk"
    - "python >= 2.7"
author: "OpenManageAnsibleEval@dell.com"

"""

EXAMPLES = """
---
- name: Export Server Configuration Profile (SCP)
  dellemc_export_server_config_profile:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       share_name: "\\\\xx.xx.xx.xx\\share"
       share_pwd:  "xxxxxxxx"
       share_user: "xxxx"
       job_wait: True
       export_format:  "XML"
       export_use:     "Default"
"""

RETURNS = """
---
dest:
    description: Exports the server configuration profile to the provided network share or to the local path.
    returned: success    
    type: string
    sample: /path/to/file.xml
"""

# log_root = '/var/log'
# dell_emc_log_path = log_root + '/dellemc'
# dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'
#
# logging.config.fileConfig(dell_emc_log_file, defaults={'logfilename': dell_emc_log_path + '/dellemc_export_scp.log'})
# # create logger
# logger = logging.getLogger('ansible')


def run_export_server_config_profile(idrac, module):
    """
    Export Server Configuration Profile to a network share

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: Exporting Server Configuration Profile Method')
    from omdrivers.enums.iDRAC.iDRACEnums import SCPTargetEnum, ExportFormatEnum, ExportUseEnum

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False

    try:
        if module.params['export_format'].lower() == 'JSON'.lower():
            export_format = ExportFormatEnum.JSON
            scp_file_name_format = "%ip_%Y%m%d_%H%M%S_scp.json"
        elif module.params['export_format'].lower() == 'XML'.lower():
            export_format = ExportFormatEnum.XML
            scp_file_name_format = "%ip_%Y%m%d_%H%M%S_scp.xml"

        logger.info(module.params['idrac_ip'] + ': CALLING: Create File share object OMSDK API')
        myshare = file_share_manager.create_share_obj(share_path=module.params['share_name'],
                                                      creds=UserCredentials(module.params['share_user'],
                                                                            module.params['share_pwd']),
                                                      isFolder=True, )
        logger.info(module.params['idrac_ip'] + ': FINISHED: Create File share object OMSDK API')

        scp_file_name = myshare.new_file(scp_file_name_format)

        target = SCPTargetEnum.ALL

        if module.params['scp_components'] == 'IDRAC':
            target = SCPTargetEnum.IDRAC
        elif module.params['scp_components'] == 'BIOS':
            target = SCPTargetEnum.BIOS
        elif module.params['scp_components'] == 'NIC':
            target = SCPTargetEnum.NIC
        elif module.params['scp_components'] == 'RAID':
            target = SCPTargetEnum.RAID
        job_wait = module.params['job_wait']

        if module.params['export_use'].lower() == 'Default'.lower():
            export_use = ExportUseEnum.Default
        elif module.params['export_use'].lower() == 'Clone'.lower():
            export_use = ExportUseEnum.Clone
        elif module.params['export_use'].lower() == 'Replace'.lower():
            export_use = ExportUseEnum.Replace

        logger.info(module.params['idrac_ip'] + ': STARTING: Exporting Server Configuration Profile Method:'
                                                ' Invoking OMSDK Export SCP API')
        idrac.use_redfish = True
        msg['msg'] = idrac.config_mgr.scp_export(scp_file_name,
                                                 target=target,
                                                 export_format=export_format,
                                                 export_use=export_use,
                                                 job_wait=job_wait)
        logger.info(module.params['idrac_ip'] + ': FINISHED: Export Server Configuration Profile Method:'
                                                ' Invoked OMSDK Export SCP API')
        if 'Status' in msg['msg'] and msg['msg']['Status'] != "Success":
            msg['failed'] = True

    except Exception as e:
        logger.error(
            module.params['idrac_ip'] + ': EXCEPTION: Exporting Server Configuration Profile Method: ' + str(e))
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
    logger.info(module.params['idrac_ip'] + ': FINISHED: Exported Server Configuration Profile Method')
    return msg, err


# Main
def main():
    module = AnsibleModule(
        argument_spec=dict(

            # iDRAC Handle
            idrac=dict(required=False, type='dict'),

            # iDRAC credentials
            idrac_ip=dict(required=True, type='str'),
            idrac_user=dict(required=True, type='str'),
            idrac_pwd=dict(required=True, type='str', no_log=True),
            idrac_port=dict(required=False, default=443, type='int'),

            # Export Destination
            share_name=dict(required=True, type='str'),
            share_pwd=dict(required=False, type='str', no_log=True),
            share_user=dict(required=False, type='str'),

            scp_components=dict(required=False,
                                choices=['ALL', 'IDRAC', 'BIOS', 'NIC', 'RAID'],
                                default='ALL'),
            job_wait=dict(required=True, type='bool'),
            export_format=dict(required=False, type='str', default='XML'),
            export_use=dict(required=False, type='str', default='Default')

        ),

        supports_check_mode=True)
    logger.info(module.params['idrac_ip'] + ': STARTING: Export Server Configuration Profile')
    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful')
    # Export Server Configuration Profile
    msg, err = run_export_server_config_profile(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: Exported Server Configuration Profile')


if __name__ == '__main__':
    main()
