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
module: virt_customize_command
short_description: Execute commands on guest image
description:
    - Execute commands on guest images
options:
  image:
    required: True
    description: Image path on filesystem
  shell:
    required: False
    description: List of commands to run in shell (commands are invoked from /usr/bin/sh), shell and command are mutually exclusive
  command:
    required: False
    description: List of commands to run directly from binaries, shell and command are mutually exclusive
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
requirements:
- "libguestfs"
- "libguestfs-devel"
- "python >= 2.7.5 || python >= 3.4"
author:
    - Vadim Khitrin (@vkhitrin)
'''

EXAMPLES = '''
- name: Executes a shell command
  virt_customize_command:
    image: /tmp/rhel7-5.qcow2
    shell: 'ls -l'

- name: Executes several shell commands
  virt_customize_command:
    image: /tmp/rhel7-5.qcow2
    shell:
      - 'ls -l'
      - 'cat /path/to/no/file'
      - 'echo a'

- name: Executes binaries with no access to network
  virt_customize_command:
    image: /tmp/rhel7-5.qcow2
    command: 'systemctl reboot'
    network: False
'''

RETURN = '''
- msg:
    type: string
    when: failure
    description: contains the error message (may include python exceptions)
    example: "cat: /fgdfgdfg/dfgdfg: No such file or directory"

- shell:
    type: dictionary
    when: success
    description: when using 'shell' argument, contains a dictionary of command and result
    example:
        "ls": {
            "stderr": "",
            "stdout": "bin\nboot\ndev\netc\nhome\nlib\nlib64\nmedia\nmnt\nopt\nproc\nroot\nrun\nsbin\nsrv\nsys\ntmp\nusr\nvar\n",
            "stdout_lines": [
                "bin",
                "boot",
                "dev",
                "etc",
                "home",
                "lib",
                "lib64",
                "media",
                "mnt",
                "opt",
                "proc",
                "root",
                "run",
                "sbin",
                "srv",
                "sys",
                "tmp",
                "usr",
                "var",
                ""
            ]
        }

- command:
    type: dictionary
    when: success
    description: when using 'command' argument, contains a dictionary of command and result
    example:
        "ls": {
            "stderr": "",
            "stdout": "bin\nboot\ndev\netc\nhome\nlib\nlib64\nmedia\nmnt\nopt\nproc\nroot\nrun\nsbin\nsrv\nsys\ntmp\nusr\nvar\n",
            "stdout_lines": [
                "bin",
                "boot",
                "dev",
                "etc",
                "home",
                "lib",
                "lib64",
                "media",
                "mnt",
                "opt",
                "proc",
                "root",
                "run",
                "sbin",
                "srv",
                "sys",
                "tmp",
                "usr",
                "var",
                ""
            ]
        }
'''

from ansible.module_utils.libguestfs.libguestfs import guest
from ansible.module_utils.basic import AnsibleModule

import re


def execute(guest, module):

    results = {
        'changed': False,
        'failed': False,
    }
    err = False

    # Create a command list
    if module.params['shell']:
        commands = module.params['shell']
        exec_method = 'shell'
    elif module.params['command']:
        commands = module.params['command']
        exec_method = 'command'

    results[exec_method] = {}

    for cmd in commands:
        try:
            if module.params['shell']:
                result = guest.sh(cmd)
            elif module.params['command']:
                # Split sentence into words using regular expressions
                cmd_args = re.findall(r'([^\s]+)', cmd)
                result = guest.command(cmd_args)
        except Exception as e:
            err = True
            results['failed'] = True
            error_message = results['msg'] = str(e)

        # Init command dict
        results[exec_method][cmd] = dict.fromkeys(['stdout', 'stdout_lines', 'stderr'], '')

        if not err:
            results['changed'] = True
            results[exec_method][cmd]['stdout'] = result
            results[exec_method][cmd]['stdout_lines'] = result.split('\n')

        else:
            results[exec_method][cmd]['stdout'] = error_message

    return results, err


def main():

    mutual_exclusive_args = [['command', 'shell']]
    required_one_of_args = [['command', 'shell']]
    module = AnsibleModule(
        argument_spec=dict(
            image=dict(required=True, type='str'),
            automount=dict(required=False, type='bool', default=True),
            network=dict(required=False, type='bool', default=True),
            selinux_relabel=dict(required=False, type='bool', default=False),
            command=dict(required=False, type='list'),
            shell=dict(required=False, type='list'),
            debug=dict(required=False, type='bool', default=False),
        ),
        mutually_exclusive=mutual_exclusive_args,
        required_one_of=required_one_of_args,
        supports_check_mode=False
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
