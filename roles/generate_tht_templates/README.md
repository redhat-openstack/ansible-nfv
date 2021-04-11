# Generate THT templates

## Description
The `generate_tht_templates` role performs generation of the OSP TripleO templates based on the user input.  
The execution of the role requires `netaddr` package. The package is a part of the requirements.txt

### Currently supported versions
* 13/16.1/16.2
  * Ovs flat/vlan/vxlan/geneve ctlplane dataplane bonding
  * Ovs vlan/vxlan/geneve DPDK ctlplane dataplane bonding
  * Ovs vlan/vxlan/geneve SRIOV ctlplane dataplane bonding
All the above scenarios supported in both standard and nic-partitioning topologies

## Run triggers
* undercloud_conf - Generates `undercloud.conf` file.
* instackenv - Generates `instackenv.json` file.
* dpdk - Generates dpdk config file.
* sriov - Generates sriov config file.
* iface_mapping - Generates `os-net-config-mappings` file.
* api_policies - Adds `api_policies.yaml` file. Used for testing.

***
Adapt the variables according to your system and generate the templates using them.  
Refer to `samples/` folder for configuration examples.

```
ansible-playbook playbooks/tripleo/generate_tht_templates.yml -e @my_vars.yml
```
