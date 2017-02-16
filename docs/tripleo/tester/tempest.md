# Tempest

## Description
Tempest role will perform the following steps:
  - Install Tempest
  - Install NFV Tempest plugin
  - Configure Tempest
  - Run defined tests

## Role tags
* run_tempest_test - Executes only the tempest tests.

## Role variables
#### Default variables
SSH user for the testing image.  
Default user: centos.
```
image_ssh_user: centos
```

Tempest test image.  
Default image: CentOS-7.
```
osp_image: http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
```

Private key and overcloud username for establishing connection between undercloud and overcloud nodes.  
Used for gathering various data like aggregation groups, etc...
```
private_key_dest: /home/stack/.ssh/id_rsa
user_for_overcloud_nodes: heat-admin
```

Port vnic type.  
Uncomment the following value in order to set the port to 'direct' type.  
Used for SR-IOV tests.  
Default value: normal. Used for standard and DPDK instances tests.
```
#port_vnic_type: direct
```

Specify the flavor that should be used during the tempest testing.  
Property values could be provided as an option.  
Multiple flavors could be created, but as by the tempest design,
only one flavor (first), could be used within the tests.  
This could be overridden by custom tempest plugins like tempest-nfv-plugin.
```
test_flavors:
  - name: nfv-test-flavor
    ram: 4096
    disk: 20
    vcpus: 4
    property:
      - "hw:mem_page_size=1GB"
      - "hw:numa_mempolicy=preferred"
      - "hw:numa_mem.0=4096"
      - "hw:numa_nodes=1"
      - "hw:numa_cpus.0=0,1,2,3"
      - "hw:cpu_policy=dedicated"
```

Flavor id that should be used for tempest tests.  
If not specified, default (first flavor in list) used.
```
#tempest_flavor_id:
```

List of tempest tests that should be executed.
```
tempest_tests:
  - tempest.scenario.test_server_basic_ops.TestServerBasicOps
```
