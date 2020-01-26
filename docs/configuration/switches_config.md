# Switches config

## Description
The switches config play performs the following tasks:
- VLAN configuration access/trunk on the switch port.
- MTU configuration on the switch port.

Supported switch platforms:
- Cisco
- Juniper

## Inventory
The play requires an inventory file that will describe switches that the play should run on.  
**Note** - Switches are static resources that not changing frequently.  
As a result the inventory could be static and not generated dynamically.  
The inventory for this play should be created by the user.

```
[ios]
switch01 ansible_host=10.10.10.100

[junos]
switch02 ansible_host=10.10.10.101

[switches:children]
ios
junos

[switches:vars]
ansible_user=root

[ios:vars]
ansible_network_os=ios
ansible_connection=network_cli
ansible_become=yes
ansible_become_method=enable

[junos:vars]
ansible_network_os=junos
ansible_connection=netconf
```

## Variables
The names of the switches in the variables should represent the name of the switch in the inventory.

```
switch01:
  vlans:
    - start: 10
      end: 20
    - start: 50
      end: 55
  interfaces:
    - { description: 'host1_port1', iface: 'xe-0/0/0', iface_mode: 'access', vlan: '10', mtu: '9000' }
    - { description: 'host2_port3', iface: 'xe-0/0/1', iface_mode: 'trunk', vlan: '15-20', mtu: '9000' }
    - { description: 'host3_port1', iface: 'xe-0/0/4', iface_mode: 'trunk', vlan: '50-53' }

switch02:
  vlans:
    - start: 25
      end: 30
    - start: 70
      end: 75
  interfaces:
    - { description: 'host1_port1', iface: 'xe-0/0/0', iface_mode: 'trunk', vlan: '25-27', mtu: '9000' }
    - { description: 'host2_port3', iface: 'xe-0/0/1', iface_mode: 'access', vlan: '29', mtu: '9000' }
    - { description: 'host3_port1', iface: 'xe-0/0/4', iface_mode: 'trunk', vlan: '70-75' }
```
