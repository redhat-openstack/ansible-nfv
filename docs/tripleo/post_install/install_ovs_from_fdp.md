# Install Custom OVS Version From FDP - Post Deployment

## Description

**NOTE:** This playbook requires a present RHOS deployment  
**NOTE:** Inventory file must be generated using `playbooks/tripleo/post_install/tripleo_inventory.yml` playbook, refer to [documentation](/docs/tripleo/post_install/tripleo_inventory.md).  
**NOTE:** This playbook may execute `rpm` commands which will make RPMDB go out of sync, if this bothers you, refer to [Red Hat's KB](https://access.redhat.com/solutions/62321)

## Preparing And Validating Environment

This playbook requires to have a virtual environment with `openstacksdk` configured on `undercloud` node, a user can opt out of this configuration if it is already configured by supplying the variable `skip_openstack_setup`.  
The playbook will be executed by default on all overcloud nodes that are part of `overcloud_nodes` Ansible group, this can be changed using the variable `node_group`.  
If Overcloud is populated with guests, by default the playbook will fail and prompt the user, this can be skipped by using the variable `skip_overcloud_check`.

### Environment Specific Variables
Ansible group to be used as part of workflow:

`overcloud_nodes` by default
```
node_group: overcloud_nodes
```

Skip necessary OpenStack Overcloud setup:

`False` by default
```
skip_openstack_setup: False
```

Skip Overcloud population validation:

`False` by default
```
skip_overcloud_check: False
```

Virtual environment to use  
(OpenStack Ansible modules require to have OpenStack python SDK installed)  
(Leverages the task `setup_openstack_env` from `roles/post_install/openstack_tasks`)

`'/tmp/ansible_venv'` by default
```
venv_path: '/tmp/ansible_venv'
```

Name of cloud to be queried via OpenStack Ansible modules  
(Requires `clouds.yaml` to be present, refer to [documentation](https://docs.openstack.org/python-openstackclient/pike/configuration/index.html))  
(Leverages the task `setup_openstack_env` from `roles/post_install/openstack_tasks`)

`'overcloud'` by default
```
query_cloud: 'overcloud'
```

Validate HTTPS certificates when using APIs:

`False` by default
```
cloud_validate_certs: False
```

### FDP Variables

URL of FDP YUM repo file:

`'http://openvswitch-ci.usersys.redhat.com/staging/7Server/x86_64/fast-datapath/fast-datapath-staging.repo'` by default
```
remote_fdp_repo_file: 'http://openvswitch-ci.usersys.redhat.com/staging/7Server/x86_64/fast-datapath/fast-datapath-staging.repo'
```

Local path of FDP yum repo file to be created:
`'/etc/yum.repos.d/fast-datapath-staging.repo'` by default.
```
local_fdp_repo_file: '/etc/yum.repos.d/fast-datapath-staging.repo'
```

### OVS Variables

OVS systemd daemons to monitor and control:

`['ovs-vswitchd.service', 'ovsdb-server.service']` by default.
```
ovs_systemd_daemons: ['ovs-vswitchd.service', 'ovsdb-server.service']
```

Trigger to perform OVS uninstall workflow if possible:

`True` by default
```
uninstall_ovs: True
```

Trigger to perform OVS installation workflow if possible:

`True` by default
```
install_ovs: True
```

OVS string regex to use to detect relevant OVS RPMs:

`'^openvswitch(\d\.\d+)?$'` by default

```
ovs_name_regex: '^openvswitch(\d\.\d+)?$'
```

Substring to be attempted to be located in available remote OVS RPMs:

**NOT DEFINED** by default.
```
install_ovs_version: 2.11
```

## Example

Examples of running the playbook:

Attempt to install OVS version containing substring `2.11`:
```
ansible-playbook playbooks/tripleo/post_install/install_ovs_from_fdp.yml -e install_ovs_version=2.11
```

Attempt to install OVS version containing substring `2.11` while skipping OpenStack virtual environment preparation and Overcloud population validation:
```
ansible-playbook playbooks/tripleo/post_install/install_ovs_from_fdp.yml -e skip_overcloud_check=True -e skip_openstack_setup=True -e install_ovs_version=2.11
```