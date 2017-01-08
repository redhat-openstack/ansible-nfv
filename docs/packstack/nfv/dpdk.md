# DPDK Role

## Description
The role sets OVS DPDK post install configuration on installed Openstack environment.  
The playbook has been tested on the following network interface:
  - **Intel Corporation Ethernet 10G 2P X520 Adapter**

## Role variables
```
hugepages_size: 1GB
```
Sets the size of the huge pages on the system.

```
hugepages_count: 16
```
Sets the count of the huge pages.

```
cores_ovs: 2
```
Core number or list of cores separated by comma, that will be used by OVS DPDK.

```
dpdk_nic_name: enp5s0f1
```
Interface name that will be used as a DPDK inteface.

```
bridge_vlan_name: br-vlan
```
The name of the bridge that will hold the DPDK interface.

```
physical_network: physnet
```
Name of the physical network that is used for DPDK networking.

```
#list_pmds: 4,20,6,22
```
The following value sets the number of PMD the openvswitch will use, please provide them as list.  
In case of HT mode, please use sibling threads.

**Note** - The value of the 'list_pmds' is not required, and disabled by default. Uncomment the value in order to apply the set.
