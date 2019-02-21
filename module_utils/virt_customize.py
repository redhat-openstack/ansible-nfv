#!/usr/vin/env python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Vadim Khitrin <me at vkhitrin.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import re

try:
    import guestfs
    HAS_GUESTFS = True
except ImportError:
    HAS_GUESTFS = False


def compare(a, b):
    return len(a) - len(b)


class guest():

    def __init__(self, module):

        if HAS_GUESTFS is False:
            results = {}
            results['msg'] = "libguestfs Python bindings are required for this module"
            self.module.fail_json(**results)

        self.mount = False
        self.automount = False
        self.module = module
        self.handle = None
        self.network = False
        self.image = None
        self.se_relabel = False
        self.debug = False

    def bootstrap(self):

        results = {}
        ansible_module_params = self.module.params
        self.image = ansible_module_params.get('image')
        self.automount = ansible_module_params.get('automount')
        self.network = ansible_module_params.get('network')
        self.debug = ansible_module_params.get('debug')
        if os.path.exists(self.image) is False:
            results['msg'] = 'Could not find image'
            self.module.fail_json(**results)

        g = guestfs.GuestFS(python_return_dict=True)
        g.add_drive_opts(self.image, readonly=0)

        if self.network:
            g.set_network(True)

        try:
            g.launch()
        except Exception as e:
            results['msg'] = 'Could not mount guest disk image' 
            if self.debug:
                results['debug'] = str(e)
            self.module.fail_json(**results)

        if self.automount:
            roots = g.inspect_os()
            if len(roots) == 0:
                results['msg'] = "No devices were found in guest disk image"
                self.module.fail_json(**results)
            for root in roots:
                mps = g.inspect_get_mountpoints(root)
                for device in sorted(mps.keys(), compare):
                    try:
                        g.mount(mps[device], device)
                    except RuntimeError as e:
                        results['msg'] = "Couldn't mount device inside guest disk image"
                        if self.debug:
                            results['debug'] = str(e)
                        self.module.fail_json(**results)
                self.mount = True

        self.handle = g
        return g

    def close(self):


        self.image = self.module.params.get('image')
        if self.handle:
            if self.mount:
                # Relabel SELinux contexts
                if self.se_relabel:
                    selinux_config = self.handle.read_lines("/etc/selinux/config")
                    re_policy = re.compile("SELINUXTYPE=(?P<policy>.*)")
                    if re_policy:
                        self.handle.rm_f("/.autorelabel")
                        selinux_policy_line = list(filter(re_policy.match, selinux_config))
                        if selinux_policy_line:
                            selinux_policy_string = re.search(re_policy, selinux_policy_line[0])
                            selinux_policy = selinux_policy_string.group('policy')
                            selinux_spec_file = "/etc/selinux/{}/contexts/files/file_contexts".format(selinux_policy)
                            if self.handle.exists(selinux_spec_file) == 1L:
                                self.handle.selinux_relabel(selinux_spec_file, "/", force=True)
                    else:
                        self.handle.touch("/.autorelabel")
                self.handle.umount_all()
            # Backwards compatability, autosync is enabled by default since libguestfs 1.5.24
            self.handle.sync()
            # Shut off applicance before closing handle
            self.handle.shutdown()
            self.handle.close()
            return True

        return False
