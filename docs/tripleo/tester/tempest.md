# Tempest

## Description
Tempest role will perform the following steps:
  - Install Tempest
  - Install NFV Tempest plugin
  - Configure Tempest
  - Run defined tests

Upstream - Install an Openstack tempest.   
Downstream - Install an RedHat tempest. The RedHat tempest is deprecated.   

**Note!** - As a default behavior, upstream tempest will be deployed upon to each playbook run.   
In order to use downstream tempest version, add "-e tempest_ver=downstream"  option to your initial playbook run.

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
**Note!** - Port vnic type options, is only usable by the downstream tempest deployment.
```
#port_vnic_type: direct
```

Flavor name that should be used for tempest tests.  
The flavor that should be created for the tempest test, specified within the openstack_tasks play.  
If not specified, default (first flavor in list) used.
```
#tempest_flavor_name:
```

Path to the tempest config file.  
Variables within the config file will be used by the tempest-nfv-plugin for the tests.  
```
tempest_config: /path/to/the/local/config/file.yml
```

Example of the tempest-nfv-plugin test configuration.  
**Note!** - The tempest config file may include additional variable such as network, images, etc... from the openstack_tasks role.
```
tests-setup:
  - name: numa0
    flavor: m1.medium.huge_pages_cpu_pinning_numa_node-0
    availability-zone:
```

List of tempest tests that should be executed.
```
tempest_tests:
  - tempest.scenario.test_server_basic_ops.TestServerBasicOps
```
