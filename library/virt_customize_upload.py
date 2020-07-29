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
module: virt_customize_upload
short_description: Uploads files to guest image
description:
    - Uploads files to guest image
options:
  image:
    required: True
    description: Image path on filesystem
  src:
    required: True
    description: Source file path on filesystem
  dest:
    required: True
    description: Destination file path in guest image
  recursive:
    required: False
    description: Copies nested directories from a directory on guest disk image
  automount:
    required: False
    description: Whether to perform auto mount of mountpoints inside guest disk image (REQUIRED for this module)
    default: True
  selinux_relabel:
    required: False
    description: Whether to perform SELinux context relabeling
  network:
    required: False
    description: Whether to enable network for appliance
    default: True
notes:
  - If your Ansible host is not your Ansible Controller host, use the module 'copy' to copy files to Ansible Host
requirements:
- "libguestfs"
- "libguestfs-devel"
- "python >= 2.7.5 || python >= 3.4"
author:
    - Vadim Khitrin (@vkhitrin)
'''

EXAMPLES = '''
- name: Upload a file to a directory in guest disk image
  virt_customize_upload:
    image: /tmp/rhel7-5.qcow2
    src: '/tmp/file.log'
    dest: '/tmp/'

- name: Upload a file and rename it on guest disk image
  virt_customize_upload:
    image: /tmp/rhel7-5.qcow2
    src: '/tmp/file.log'
    dest: '/tmp/MYFILE.log'

- name: Upload a directory to guest disk image
  virt_customize_upload:
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
    description: source path of file(s) on host
    example: "/tmp/RESULT_ANS.log"

- dest:
    type: string
    when: always
    description: dest path of file(s) on guest image
    example: "/tmp/RESULT_ANS.log"

- md5:
    type: string
    when: success upload file
    description: displays md5 checksum of file
    "debug": "d6fe77f000341b5f9a952e744f34901a"
'''

from ansible.module_utils.libguestfs.libguestfs import guest
from ansible.module_utils.basic import AnsibleModule

import os


def upload(guest, module):

    err = False
    results = {
        'changed': False,
        'failed': False
    }
    md5sum_src = None
    md5sum_dest = None
    src = module.params['src']
    dest = module.params['dest']

    if not os.path.exists(src):
        err = True
        results['failed'] = True
        results['msg'] = 'Source path {path} not found'.format(path=src)

    elif not os.access(src, os.R_OK):
        err = True
        results['failed'] = True
        results['msg'] = 'Source path {path} not accessable'.format(path=src)

    if not err:
        try:
            # Check if source path is a file and not a directory/symlink
            if not os.path.isfile(src) and not module.params['recursive']:
                err = True
                results['msg'] = "Source file is either directory or symlink, if it's a directory use 'recursive' argument"
            else:
                if module.params['recursive']:
                    guest.copy_in(src, dest)
                    if not src.endswith(os.path.sep):
                        dest = dest + os.path.basename(src)
                else:
                    md5sum_src = module.md5(src)
                    if dest.endswith(os.path.sep):
                        dest = dest + os.path.basename(src)
                    # Check if destination file exists on guest image
                    if guest.is_file(dest):
                        md5sum_dest = guest.checksum("md5", dest)
                    # If md5sum of source file and dest file are different, upload file to guest
                    if md5sum_src != md5sum_dest:
                        results['changed'] = True
                        guest.upload(src, dest)

        except Exception as e:
            err = True
            results['failed'] = True
            results['msg'] = str(e)

        if md5sum_src:
            md5sum_dest = guest.checksum("md5", dest)

        if not err:
            results['src'] = src
            '''
            Not using 'dest' in results due to
            'ansible.module_utils.basic' containing the method
            'add_path_info' which attempts to retrieve info
            regarding the path which does not exist on target host
            (Fixed in Ansible 2.8,
            commit: cc9c72d6f845710b24e952670b534a57f6948513)
            '''
            results['guest_dest'] = dest

            if md5sum_src and md5sum_dest:
                results['md5'] = md5sum_src

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
    results, err = upload(instance, module)
    g.close()

    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
