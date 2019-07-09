# Dynaminc Host Inventory

## Description

The following role adds an instance to dynamic(in-memory) inventory.

This role can leverage `roles/post_install/discover_instance_ports` and attempt to dicover management IP(Floatin IP) from OpenStack APIs.

This role requires to have [clouds.yaml](https://docs.openstack.org/python-openstackclient/rocky/configuration/index.html) which can be generated using task `setup_openstack_env` in role `roles/post_install/openstack_task`.

## Invocation

This role recieves a list of dictionaries and performs accordingly, here is a sample playbook which attemps to dicover management IP addresses:
```
---
- hosts: undercloud
  gather_facts: False
  pre_tasks:
    - block:
        - name: Prepare Virtual Environment
          include_role:
            name: roles/post_install/openstack_tasks
            tasks_from: setup_openstack_env

        - include_role: 
            name: roles/post_install/dynamic_host_inventory
          loop: "{{ dynamic_instances }}"

- hosts: trex
  gather_facts: False
  tasks:
    - shell: 'ls'

- hosts: dut
  gather_facts: False
  tasks:
    - shell: 'ls'
```

With the following extra variables passed to playbook:
```
discover_instance_external_ip: True
dynamic_instances:
  - name: trex
    group: trex
    user: cloud-user
    ssh_key: /tmp/test_keypair.key
  - name: testpmd_dpdk_dut
    group: dut
    user: cloud-user
    ssh_key: /tmp/test_keypair.key
```

## Role Variables

Assuming `dynamic_instances` was passed to role:
```
dynamic_instances:
  - name: vm1 # Name of instance to be queried against OpenStack APIs if attempting to disover IP address
            # Can be omitted if not discovering via OpenStack APIs
    group: vm_group # Name of group to assign the instance to
    user: root # Username to authenticate with
    password: password # Password to authenticate with, can be omitted if using SSH key
    ssh_key /path/to/key # SSH key used to authenticate with_
    ssh_pass: passphrase # SSH passphrase used to unlock SSH key
    mgmt_ip: 1.1.1.1 # Management IP of instance
                   # Can be specified or attempted to be discovered from OpenStack APIs
                   # Will override automatically discovered IP address
    cloud: overcloud # Name of cloud to be used when querying instance, can be omitted
                   # Requires clouds.yaml to be present on Ansible host, refer to:
                   # https://docs.openstack.org/os-client-config/latest/user/configuration.html#site-specific-file-locations
    cert_validate: False # Whether to validate SSL certificates when querying cloud, False by default
 - name: vm2
    group: vm_group
    user: root
    password: password
    ssh_key /path/to/key
    ssh_pass: passphrase
    mgmt_ip: 1.1.1.1
    cloud: overcloud
    cert_validate: False # Whether to validate SSL certificates when querying cloud, False by default
```

Whether to attempt to discover management IP address using OpenStack APIs:
```
discover_instance_external_ip: True
```