#!/usr/vin/env python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Vadim Khitrin <me at vkhitrin.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
module: virt_customize_download
short_description: Downloads files/directories from guest disk image
version_added: "2.5.11"
description:
    - Downloads files/directories from guest disk image
options:
    image:
        required: True
        description: image path on filesystem.
    src:
        required: True
        description: source file path on guest disk image.
    dest:
        required: True
        description: dest file path on host
    remote_src:
        required: True
        description: perform copy of source file from remote host instead on ansible host.
    recursive:
        required: False
        description: copies nested directories to a directory on guest disk image.
    automount:
        required: False
        description: Whether to perform auto mount of mountpoints inside guest disk image (REQUIRED for this module)
        default: True
    network:
        required: False
        description: Whether to enable network for appliance
        default: True
    selinux_relabel:
        required: False
        description: Whether to perform SELinux contect relabeling during invocation

---
requirements:
    - "guestfs"
    - "python >= 2.7.5"
author: Vadim Khitrin (@vkhitrin)

"""

EXAMPLES = """
---
- name: Download a file from guest disk image
  virt_customize_download:
    image: /tmp/rhel7-5.qcow2
    src: '/tmp/file.log'
    dest: '/tmp/'

- name: Download a file and rename it on host
  virt_customize_download:
    image: /tmp/rhel7-5.qcow2
    src: '/tmp/file.log'
    dest: '/tmp/MYFILE.log'

- name: Download a directory from guest disk image
  virt_customize_download:
    image: /tmp/rhel7-5.qcow2
    src: '/tmp/logs/'
    dest: '/tmp/'
    recursive: True
"""

RETURN = """
- msg:
    type: string
    when: failure
    description: Contains the error message (may include python exceptions)
    example: "read: /tmp/aaaa: Is a directory'

- results:
    type: dictionary
    when: success
    description: Contains the module successful execution results
    example: {
        "dest": "/tmp/RESULT_ANS.log",
        "src": "/tmp/RESULT_ANS.log"
    }

- md5:
    type: string
    when: success upload file
    description: displays md5 checksum of file
    "debug": "d6fe77f000341b5f9a952e744f34901a"

"""

from ansible.module_utils.virt_customize import guest
from ansible.module_utils.basic import AnsibleModule

import os

def download(guest, module):

    err = False
    results = {
        'changed': False,
        'failed': False
    }
    md5sum_src = md5sum_dest = None

    if module.params['automount']:
       try:
           if module.params['recursive']:
               guest.copy_out(module.params['src'], module.params['dest'])
               if not module.params['src'].endswith(os.path.sep):
                   module.params['dest'] = module.params['dest'] + os.path.basename(module.params['src'])
           else:
               if module.params['dest'].endswith(os.path.sep):
                   module.params['dest'] = module.params['dest'] + os.path.basename(module.params['src'])
               guest.download(module.params['src'], module.params['dest'])
       except Exception as e:
           err = True
           results['failed'] = True
           results['msg'] = str(e)

       if md5sum_src:
           md5sum_dest = guest.checksum("md5", module.params['dest'])

       if md5sum_src != md5sum_dest:
           err = True
           results['failed'] = True
           results['msg'] = 'Uploaded file does not match source file md5 checksum'

       if not err:
           results['changed'] = True
           results['result'] = {
               'src': module.params['src'],
               'dest': module.params['dest']
           }

           if md5sum_src and md5sum_dest:
               results['md5'] = md5sum_src 

    else:
        err = True
        results['msg'] = "automount is false, can't proceed with this module"

    return results, err


def main():

    module = AnsibleModule(
        argument_spec=dict(
            image=dict(required=True, type='str'),
            src=dict(required=True, type='path'),
            dest=dict(required=True, type='path'),
            remote_src=dict(required=False, type='bool', default=False),
            recursive=dict(required=False, type='bool', default=False),
            automount=dict(required=False, type='bool', default=True),
            network=dict(required=False, type='bool', default=True),
            selinux_relabel=dict(required=False, type='bool', default=False),
        ),
        supports_check_mode=True
    )

    g = guest(module)
    instance = g.bootstrap()
    results, err = download(instance, module)
    g.close()

    if err:
        module.fail_json(**results)
    module.exit_json(**results)

if __name__ == '__main__':
    main()
