# DPDK Role

## Description
***
**Note** - DPDK post install configuration role applies only to the following OSPd/TripleO versions:

* Liberty (8)
* Mitaka (9)

Starting from Newton (10) version, OVS DPDK feature is fully supported by OSPd/TripleO heat templates.

***

The role sets OVS DPDK post install configuration on installed Openstack environment.  
The playbook has been tested on the following network interface:
  - **Intel Corporation Ethernet 10G 2P X520 Adapter**

## Role variables
Sets the size of the huge pages on the system.
```
hugepages_size: 1GB
```

Sets the count of the huge pages.
```
hugepages_count: 16
```

Core or list of cores separated by comma, that will be used by OVS DPDK.
```
cores_ovs: 2
```

Interface name that will be used as a DPDK inteface.
```
dpdk_nic_name: enp5s0f1
```

The name of the bridge that will hold the DPDK interface.
```
bridge_vlan_name: br-vlan
```

Name of the physical network that is used for DPDK networking.
```
physical_network: physnet
```

The following value sets the number of PMD the openvswitch will use, please provide them as list.  
In case of HT mode, please use sibling threads.
```
#list_pmds: 4,20,6,22
```

**Note** - The value of the 'list_pmds' is not required, and disabled by default. Uncomment the value in order to apply the set.
