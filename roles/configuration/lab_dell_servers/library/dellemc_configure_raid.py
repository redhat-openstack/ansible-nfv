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
from omdrivers.enums.iDRAC.BIOS import *
from omdrivers.types.iDRAC.RAID import *
# from omsdk.sdkfile import FileOnShare
# import logging.config

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: dellemc_configure_raid
short_description: Configures the RAID configuration attributes.
version_added: "2.3"
description:
    - This module is responsible for configuring the RAID attributes.
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
        description: Network share user password.
    share_mnt:
        required: False
        description: Local mount path of the network share with read-write permission for ansible user.
    vd_name: 
        required: False
        description: Virtual disk name. 
          - optional, if we will perform create operations
          - mandatory, if we will perform remove operations
    span_depth:
        required: False
        description: Span Depth
        default: 1
    span_length:
        required: False
        description: Span Length
        default: 2
    number_dedicated_hot_spare:
        required: False
        description: Number of Dedicated Hot Spare
        default: 0
    number_global_hot_spare:
        required: False
        description: Number of Global Hot Spare
        default: 0  
    raid_level:
        required: False
        description: Provide the the required RAID level
        choices: ['RAID 0', 'RAID 1', 'RAID 5', 'RAID 6', 'RAID 10', 'RAID 50', 'RAID 60']
        default: "RAID 0"
    disk_cache_policy:
        required: False
        description: Disk Cache Policy
        choices: ["Default", "Enabled", "Disabled"]
        default: Default
    write_cache_policy:
        required: False
        description: Write cache policy
        choices: ["WriteThrough", "WriteBack", "WriteBackForce"]
        default: WriteThrough
    read_cache_policy:
        required: False
        description: Read cache policy
        choices: ["NoReadAhead", "ReadAhead", "Adaptive"]
        default: NoReadAhead
    stripe_size:
        required: False
        description: Stripe size value to be provided in multiples of 64 * 1024
        default: 65536
    controller_fqdd:
        required:  True
        description: Fully Qualified Device Descriptor (FQDD) of the storage controller, for e.g. 'RAID.Integrated.1-1'.
    media_type:
        required:  False
        description: Media type
        choices: ['HDD', 'SSD']
        default: 'HDD'
    bus_protocol:
        required:  False
        description: Bus protocol
        choices: ['SAS', 'SATA']
        default: 'SATA'
    state:
        required: True
        description:
          - if present, will perform create operations
          - if absent, will perform remove operations
        choices: ['present', 'absent']
        default: None

requirements:
    - "omsdk"
    - "python >= 2.7"
author: "OpenManageAnsibleEval@dell.com"

"""

EXAMPLES = """
---
- name: Configure the Raid attributes.
  dellemc_configure_raid:
       idrac_ip:   "xx.xx.xx.xx"
       idrac_user: "xxxx"
       idrac_pwd:  "xxxxxxxx"
       share_name: "\\\\xx.xx.xx.xx\\share"
       share_pwd:  "xxxxxxxx"
       share_user: "xxxx"
       share_mnt: "/mnt/share"
       state: "xxxx"
       controller_fqdd:"xxxxxxxx"
       vd_name:  "xxxxxx"
"""

RETURNS = """
---
- dest:
    description: Configures the Raid configuration attributes.
    returned: success
    type: string
"""

# log_root = '/var/log'
# dell_emc_log_path = log_root + '/dellemc'
# dell_emc_log_file = dell_emc_log_path + '/dellemc_log.conf'
#
# logging.config.fileConfig(dell_emc_log_file, defaults={'logfilename': dell_emc_log_path + '/dellemc_raid_config.log'})
# # create logger
# logger = logging.getLogger('ansible')


def run_server_raid_config(idrac, module):
    """
    Get Lifecycle Controller status

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """
    logger.info(module.params['idrac_ip'] + ': STARTING: Raid config method')
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
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

        if module.params['state'] == "present":
            # Create VD
            logger.info(module.params['idrac_ip'] + ': CALLING: Raid config : Create virtual disk  OMSDK API')

            # Physical Disk filter
            pd_filter = '((disk.parent.parent is Controller and disk.parent.parent.FQDD._value == "{0}")'.format(
                module.params['controller_fqdd'])
            pd_filter += ' or (disk.parent is Controller and disk.parent.FQDD._value == "{0}"))'.format(
                module.params['controller_fqdd'])
            pd_filter += ' and disk.MediaType == "{0}"'.format(module.params['media_type'])
            pd_filter += ' and disk.BusProtocol == "{0}"'.format(module.params['bus_protocol'])

            msg['msg'] = idrac.config_mgr.RaidHelper.new_virtual_disk(
                # VirtualDisk parameters
                Name=module.params['vd_name'],
                SpanDepth=module.params['span_depth'],
                SpanLength=module.params['span_length'],
                NumberDedicatedHotSpare=module.params['number_dedicated_hot_spare'],
                NumberGlobalHotSpare=module.params['number_global_hot_spare'],
                RAIDTypes=module.params['raid_level'],
                DiskCachePolicy=module.params['disk_cache_policy'],
                RAIDdefaultWritePolicy=module.params['write_cache_policy'],
                RAIDdefaultReadPolicy=module.params['read_cache_policy'],
                StripeSize=module.params['stripe_size'],
                RAIDforeignConfig="Clear",
                RAIDaction=RAIDactionTypes.Create,
                PhysicalDiskFilter=pd_filter
                )
            logger.info(module.params['idrac_ip'] + ': FINISHED: Raid config : Create virtual disk  OMSDK API')

        if module.params['state'] == "absent":
            # Remove VD
            logger.info(module.params['idrac_ip'] + ': CALLING: Raid config : Remove virtual disk  OMSDK API')
            if module.params['vd_name'] == None:
                message = 'Virtual disk name is a required parameter for remove virtual disk operations.'
                err = True
                msg['msg'] = "{}".format(message)
                msg['failed'] = True
                logger.info(module.params['idrac_ip'] + ': FINISHED: {}'.format(message))
                return msg, err
            msg['msg'] = idrac.config_mgr.RaidHelper.delete_virtual_disk(Name=module.params['vd_name'])
            logger.info(module.params['idrac_ip'] + ': FINISHED: Raid config : Remove virtual disk  OMSDK API')
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
        logger.error(module.params['idrac_ip'] + ': EXCEPTION: Raid config OMSDK API')
    logger.info(module.params['idrac_ip'] + ': FINISHED: Raid config Method')
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

            # conditional variable for create or remove.
            state=dict(required=True, choices=['present', 'absent'], default=None),

            # Raid configuration Attributes
            vd_name=dict(required=False, type='str', default=None),
            span_depth=dict(required=False, type='int', default=1),
            span_length=dict(required=False, type='int', default=2),
            number_dedicated_hot_spare=dict(required=False, type='int', default=0),
            number_global_hot_spare=dict(required=False, type='int', default=0),
            raid_level=dict(required=False, type='str',
                            choices=['RAID 0', 'RAID 1', 'RAID 5', 'RAID 6', 'RAID 10', 'RAID 50', 'RAID 60'],
                            default="RAID 0"),
            disk_cache_policy=dict(required=False, type='str', choices=["Default", "Enabled", "Disabled"],
                                   default="Default"),
            write_cache_policy=dict(required=False, type='str', choices=["WriteThrough", "WriteBack", "WriteBackForce"],
                                    default="WriteThrough"),
            read_cache_policy=dict(required=False, type='str', choices=["NoReadAhead", "ReadAhead", "Adaptive"],
                                   default="NoReadAhead"),
            stripe_size=dict(required=False, type='int', default=64 * 1024),

            # pd_filter parameter
            controller_fqdd=dict(required=True, type='str'),
            media_type=dict(required=False, choices=['HDD', 'SSD'], default='HDD', type='str'),
            bus_protocol=dict(required=False, choices=['SAS', 'SATA'], default='SATA', type='str'),
        ),

        supports_check_mode=True)
    logger.info(module.params['idrac_ip'] + ': STARTING: Export Server Configuration Profile')
    # Connect to iDRAC
    logger.info(module.params['idrac_ip'] + ': CALLING: iDRAC Connection')
    idrac_conn = iDRACConnection(module)
    idrac = idrac_conn.connect()

    logger.info(module.params['idrac_ip'] + ': FINISHED: iDRAC Connection is successful')
    # Export Server Configuration Profile
    msg, err = run_server_raid_config(idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)
    logger.info(module.params['idrac_ip'] + ': FINISHED: Exported Server Configuration Profile')


if __name__ == '__main__':
    main()
