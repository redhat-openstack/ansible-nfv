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
module: virt_customize_users
short_description: Manages users in guest images
version_added: "2.4"
description:
    - Manages users in guest images
options:
    image:
        required: True
        description: image path on filesystem.
    name:
        required: True
        description: name of user
    password:
        required: False
        description: user's password
    state:
        required: True
        description: action to be performed
        choices:
          - present
          - absent
    automount:
        required: False
        description: Whether to perform auto mount of mountpoints inside guest disk image (REQUIRED for this module)
        default: True
    network:
        required: False
        description: Whether to enable network for appliance
        default: True

---
requirements:
    - "guestfs"
    - "python >= 2.7.5"
author: Vadim Khitrin (@vkhitrin)

"""

EXAMPLES = """
---
- name: Creates a user
  virt_customize_users:
    image: /tmp/rhel7-5.qcow2
    user: test_user
    password: test_password
    state: present

- name: Change password to an existing user
  virt_customize_users:
    image: /tmp/rhel7-5.qcow2
    user: root
    password: root_password
    state: present

- name: Delete a user
  virt_customize_users:
    image: /tmp/rhel7-5.qcow2
    user: root
    password: root_password
    state: absent
"""

RETURN = """
- msg:
    type: string
    when: failure
    description: Contains the error message (may include python exceptions)
    example: "cat: /fgdfgdfg/dfgdfg: No such file or directory"

- results:
    type: array
    when: success
    description: Contains the module successful execution results
    example: [
        "test_user is present"
    ]
"""

from ansible.module_utils.virt_customize import guest
from ansible.module_utils.basic import AnsibleModule

import re

def users(guest, module):

    state = module.params['state']
    user_name = module.params['name']
    user_password = module.params['password']
    results = {
        'changed': False,
        'failed': False,
        'results': []
    }
    err = False

    if module.params['automount']:
        try:
            guest.sh_lines('id -u {}'.format(user_name))
            user_exists = True
        except Exception:
            user_exists = False

        if state == 'present':
            if user_exists:
                try:
                    guest.sh_lines('{u}:{p} | chpasswd'.format(u=user_name,
                                                               p=user_password))
                except Exception as e:
                    err = True
                    results['failed'] = True
                    results['msg'] = str(e)

            else: 
                try:
                    guest.sh_lines('useradd {user}'.format(user=user_name))
                    guest.sh_lines('{u}:{p} | chpasswd'.format(u=user_name,
                                                               p=user_password))
                except Exception as e:
                    err = True
                    results['failed'] = True
                    results['msg'] = str(e)

        elif state == 'absent':
            if user_exists:
                try:
                    guest.sh_lines('userdel {user}'.format(user=user_name))
                except Exception as e:
                    err = True
                    results['failed'] = True
                    results['msg'] = str(e)

        if not err:
            results['changed'] = True
            results['results'].append('{u} is {s}'.format(u=user_name, s=state))
    return results, err


def main():

    required_togheter_args = [['name', 'state']]
    module = AnsibleModule(
        argument_spec=dict(
            image=dict(required=True, type='str'),
            automount=dict(required=False, type='bool', default=True),
            network=dict(required=False, type='bool', default=True),
            selinux_relabel=dict(required=False, type='bool', default=False),
            name=dict(required=True, type='str'),
            # TODO vkhitrin: state=absent and no password support
            password=dict(required=True, type='str', no_log=True),
            state=dict(required=True, choices=['present', 'absent']),
            debug=dict(required=False, type='bool', default=False),
            force=dict(required=False, type='bool', default=False)
        ),
        required_together=required_togheter_args,
        supports_check_mode=True
    )

    g = guest(module)
    instance = g.bootstrap()
    results, err = users(instance, module)
    g.close()

    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
