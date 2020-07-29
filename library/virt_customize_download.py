#!/usr/vin/env python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Vadim Khitrin <me at vkhitrin.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: virt_customize_download
short_description: Fetch files from guest image
description:
    - Fetch files from guest image
options:
  image:
    required: True
    description: Image path on filesystem
  src:
    required: True
    description: Source file path on guest image
  dest:
    required: True
    description: Destination file path on filesystem
  recursive:
    required: False
    description: Copies nested directories from a directory on guest disk image
    default: False
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
    description: Whether to perform SELinux context relabeling
    default: False
notes:
  - If your Ansible host is not your Ansible Controller host, use the module 'fetch' or 'synchronize' to retrieve remote files
requirements:
- "libguestfs"
- "libguestfs-devel"
- "python >= 2.7.5 || python >= 3.4"
author:
    - Vadim Khitrin (@vkhitrin)
'''

EXAMPLES = '''
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
'''

RETURN = '''
- msg:
    type: string
    when: failure
    description: Contains the error message (may include python exceptions)
    example: "read: /tmp/aaaa: Is a directory'

- src:
    type: string
    when: always
    description: source path of file(s) to download on guest image
    example: "/tmp/RESULT_ANS.log"

- dest:
    type: string
    when: always
    description: dest path of file(s) to download to host
    example: "/tmp/RESULT_ANS.log"

- md5:
    type: string
    when: successful download of a single file
    description: displays md5 checksum of single file
    "example": "d6fe77f000341b5f9a952e744f34901a"
'''

from ansible.module_utils.libguestfs.libguestfs import guest
from ansible.module_utils.basic import AnsibleModule

import os


def download(guest, module):

    err = False
    results = {
        'changed': False,
        'failed': False,
        'src': module.params['src'],
    }
    md5sum_src = None
    md5sum_dest = None
    src = module.params['src']
    dest = module.params['dest']

    try:
        # Check if source path is a file and not a directory/symlink
        if not guest.is_file(src) and not module.params['recursive']:
            err = True
            results['msg'] = "Source file is either directory or symlink, if it's a directory use 'recursive' argument"
        else:
            if module.params['recursive']:
                if not src.endswith(os.path.sep):
                    dest = dest + os.path.basename(src)
                guest.copy_out(src, dest)
            else:
                md5sum_src = guest.checksum("md5", src)
                if dest.endswith(os.path.sep):
                    dest = dest + os.path.basename(src)
                # Check if destination file exists on host
                if os.path.isfile(dest):
                    md5sum_dest = module.md5(dest)
                # If md5sum of source file and dest file are different, download file from guest
                if md5sum_src != md5sum_dest:
                    results['changed'] = True
                    guest.download(src, dest)

    except Exception as e:
        err = True
        results['failed'] = True
        results['msg'] = str(e)

    if not err:
        results['md5sum'] = md5sum_src
        results['dest'] = dest

    return results, err


def main():

    module = AnsibleModule(
        argument_spec=dict(
            image=dict(required=True, type='str'),
            src=dict(required=True, type='path'),
            dest=dict(required=True, type='path'),
            recursive=dict(required=False, type='bool', default=False),
            automount=dict(required=False, type='bool', default=True),
            network=dict(required=False, type='bool', default=True),
            selinux_relabel=dict(required=False, type='bool', default=False),
        ),
        supports_check_mode=False
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
