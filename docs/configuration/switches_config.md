# Switches config

## Description
The switches config play performs the following tasks:
- VLAN configuration access/trunk on the switch port.
- MTU configuration on the switch port.
- LACP configuration on interface and members attach.
- IGMP Snooping configuration

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
cisco_switch01 ansible_host=10.10.10.120

[junos]
juniper_switch01 ansible_host=10.10.10.100
juniper_switch02 ansible_host=10.10.10.101

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
juniper_switch01:
  vlans:
    - start: 10
      end: 20
    - start: 50
      end: 55
  interfaces:
    - { description: 'host1_port1', iface: 'xe-0/0/0', iface_mode: 'access', vlan: '10', mtu: '9000' }
    - { description: 'host2_port3', iface: 'xe-0/0/1', iface_mode: 'trunk', vlan: '15-20', mtu: '9000' }
    - { description: 'host3_port1', iface: 'xe-0/0/4', iface_mode: 'trunk', vlan: '50-53' }
    - { description: 'aggregation', iface: 'ae2', iface_mode: 'trunk', vlan: '53-55', mtu: '9192', aggr_members: ['xe-0/0/12', 'xe-0/0/13'] }
  igmp_snooping:
    - { vlan: '55', ip_address: '10.20.155.5', interfaces: ['ae2'] }

juniper_switch02:
  vlans:
    - start: 25
      end: 30
    - start: 70
      end: 75
  interfaces:
    - { description: 'host1_port1', iface: 'xe-0/0/0', iface_mode: 'trunk', vlan: '25-27', mtu: '9000' }
    - { description: 'host2_port3', iface: 'xe-0/0/1', iface_mode: 'access', vlan: '29', mtu: '9000' }
    - { description: 'host3_port1', iface: 'xe-0/0/4', iface_mode: 'trunk', vlan: '70-75' }
    - { description: 'host3_port1', iface: 'xe-0/0/5', iface_mode: 'trunk', vlan: '70' }

cisco_switch01:
  vlans:
    - start: 100
      end: 105
  interfaces:
     - { description: 'tigon15', iface: 'GigabitEthernet5/0/6', iface_mode: 'access', vlan: '20' }
     - { description: 'tigon16', iface: 'GigabitEthernet5/0/7', iface_mode: 'access', vlan: '20' }
     - { description: 'tigon17', iface: 'GigabitEthernet5/0/8', iface_mode: 'access', vlan: '90' }
     - { description: 'uplink_port', iface: 'GigabitEthernet5/0/9', iface_mode: 'trunk', vlan: '', encapsulation: true }
```
