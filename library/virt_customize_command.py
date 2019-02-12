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
module: virt_customize_command
short_description: Performs commands on guest images
version_added: "2.5.11"
description:
    - Performs commands on guest images
options:
    image:
        required: True
        description: image path on filesystem.
    shell:
        required: False
        description: List of commands to run in shell (commands are invoked from /usr/bin/sh)
    command:
        required: False
        description: List of commands to run directly from binaries
    force:
        required: False
        description: Perform all commands even if there is failures
    automount:
        required: False
        description: Whether to perform auto mount of mountpoints inside guest disk image (REQUIRED for this module)
        default: True
    network:
        required: False
        description: Whether to enable network for appliance
        default: True
    debug:
        required: False
        description: When available attempt do display debug info
        default: False

---
requirements:
    - "guestfs"
    - "python >= 2.7.5"
author: Vadim Khitrin (@vkhitrin)

"""

EXAMPLES = """
---
- name: Executes a shell command
  virt_customize_command:
    image: /tmp/rhel7-5.qcow2
    shell: 'ls -l'

- name: Executes several shell commands and doesn't quit on error
  virt_customize_command:
    image: /tmp/rhel7-5.qcow2
    shell:
      - 'ls -l'
      - 'cat /path/to/no/file'
      - 'echo a'
    force: True

- name: Executes binaries with no access to network
  virt_customize_command:
    image: /tmp/rhel7-5.qcow2
    command: 'systemctl reboot'
    network: False

- name: Run several binaries and display debug info
  virt_customize_command:
    image: /tmp/rhel7-5.qcow2
    command:
      - 'ls -lra'
      - 'ip a'
    debug: True

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
        "ls -l",
        "cat /etc/redhat-release"
    ]

- debug:
    type: dictionary
    when: available and invoked
    description: displays debug info
    "debug": {
        "ls -l": [
            "total 84",
            "drwxr-xr-x  2 root root  4096 Dec 18 14:33 bin",
            "drwxr-xr-x  4 root root  4096 Dec  3 09:52 boot",
            "drwxr-xr-x 16 root root  2640 Dec 20 13:42 dev",
            "drwxr-xr-x 87 root root  4096 Dec 20 13:43 etc",
            "drwxr-xr-x  2 root root  4096 Oct 15 17:10 home",
            "lrwxrwxrwx  1 root root    33 Dec  3 09:39 initrd.img -> boot/initrd.img-4.18.0-12-generic",
            "lrwxrwxrwx  1 root root    33 Dec  3 09:39 initrd.img.old -> boot/initrd.img-4.18.0-12-generic",
            "drwxr-xr-x 19 root root  4096 Dec  3 09:39 lib",
            "drwxr-xr-x  2 root root  4096 Dec  3 09:37 lib64",
            "drwx------  2 root root 16384 Dec  3 09:51 lost+found",
            "drwxr-xr-x  2 root root  4096 Dec  3 09:37 media",
            "drwxr-xr-x  2 root root  4096 Dec  3 09:37 mnt",
            "drwxr-xr-x  2 root root  4096 Dec  3 09:37 opt",
            "dr-xr-xr-x 74 root root     0 Dec 20 13:42 proc",
            "drwx------  2 root root  4096 Dec  3 09:40 root",
            "drwxr-xr-x  3 root root  4096 Dec  3 09:40 run",
            "drwxr-xr-x  2 root root  4096 Dec  3 09:40 sbin",
            "drwxr-xr-x  2 root root  4096 Oct 15 20:23 snap",
            "drwxr-xr-x  2 root root  4096 Dec  3 09:37 srv",
            "dr-xr-xr-x 13 root root     0 Dec 20 13:42 sys",
            "drwxrwxrwt  2 root root  4096 Dec 18 16:00 tmp",
            "drwxr-xr-x 10 root root  4096 Dec  3 09:37 usr",
            "drwxr-xr-x 13 root root  4096 Dec  3 09:40 var",
            "lrwxrwxrwx  1 root root    30 Dec  3 09:39 vmlinuz -> boot/vmlinuz-4.18.0-12-generic",
            "lrwxrwxrwx  1 root root    30 Dec  3 09:39 vmlinuz.old -> boot/vmlinuz-4.18.0-12-generic"
        ]
    } 

"""

from ansible.module_utils.virt_customize import guest
from ansible.module_utils.basic import AnsibleModule

import re

def execute(guest, module):

    results = {
        'changed': False,
        'failed': False,
        'results': []
    }
    err = False

    if module.params['debug']:
        results['debug'] = {}

    # Create a command list
    if module.params['shell']:
        commands = module.params['shell']
    elif module.params['command']:
        commands = module.params['command']

    if module.params['automount']:
        for cmd in commands:
            try:
                if module.params['shell']:
                    result = guest.sh_lines(cmd)
                elif module.params['command']:
                    # Split sentence into words using regular expressions
                    cmd_args = re.findall('([^\s]+)', cmd)
                    result = guest.command_lines(cmd_args)
            except Exception as e:
                err = True
                results['failed'] = True
                result = results['msg'] = str(e)
                
            results['results'].append(cmd)

            if module.params['debug'] and not err:
                results['debug'][cmd] = result

            if not module.params['force'] and err:
                break

    else:
        err = True
        results['msg'] = "automount is false, can't proceed with this module"

    return results, err


def main():

    mutual_exclusive_args = [['command', 'shell']]
    required_one_of_args = [['command', 'shell']]
    module = AnsibleModule(
        argument_spec=dict(
            image=dict(required=True, type='str'),
            automount=dict(required=False, type='bool', default=True),
            network=dict(required=False, type='bool', default=True),
            command=dict(required=False, type='list'),
            shell=dict(required=False, type='list'),
            debug=dict(required=False, type='bool', default=False),
            force=dict(required=False, type='bool', default=False)
        ),
        mutually_exclusive=mutual_exclusive_args,
        required_one_of=required_one_of_args,
        supports_check_mode=True
    )

    g = guest(module)
    instance = g.bootstrap()
    results, err = execute(instance, module)
    g.close()

    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
