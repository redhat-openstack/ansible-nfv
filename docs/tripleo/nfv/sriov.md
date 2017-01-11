# SRIOV Role

## Description
***
**Note** - SRIOV post install configuration role applies only to the following OSPd/TripleO versions:

* Liberty (8)
* Mitaka (9)

Starting from Newton (10) version, SRIOV feature is fully supported by OSPd/TripleO heat templates.

***

The role sets SRIOV post install configuration on installed Openstack environment.  
The playbook has been tested on the following network interface:
  - **Intel Corporation Ethernet 10G 2P X520 Adapter**
  - **Broadcom Corporation NetXtreme II BCM57810 10 Gigabit Ethernet**

## Role variables
Interface that will be used for SRIOV VNF.
```
interface: eno2
```

Physical network that is used for sriov networking.
```
physical_network: physnet
```

Use "virtual_function_number" variable if you want to override the use of total virtual function number.  
By default, it will use the amount of virtual functions the interface can provide.  
To use the variable, uncomment it, and specify the number of vfs you would like to use.
```
#virtual_function_number:
```

Install SRIOV agent. By default will be installed.
```
sriov_agent_install: true
```
