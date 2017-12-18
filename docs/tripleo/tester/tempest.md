# Tempest

## Description
Tempest role is dedicated to perform testing execution on TripleO OpenStack environments.

Tempest role will perform the following steps:
  - Install upstream Tempest
  - Install NFV Tempest plugin
  - Install Neutron Tempest plugin
  - Configure Tempest using the python-tempestconf repository
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

Provide required image that will be used for the tempest tests.  
If multiple images are provided, the first one will be used.  
Default image: CentOS-7.
```
images:
  - name: centos7
    url: http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
```

Private key and overcloud username for establishing connection between undercloud and overcloud nodes.  
Used for gathering various data like aggregation groups, etc...
```
private_key_dest: /home/stack/.ssh/id_rsa
user_for_overcloud_nodes: heat-admin
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

List of tempest tests that should be executed.
```
tempest_tests:
  - tempest_nfv_plugin.tests.scenario.test_nfv_epa.TestBasicEpa.test_numa0_provider_network
  - tempest_nfv_plugin.tests.scenario.test_nfv_epa.TestBasicEpa.test_numa1_provider_network
  - tempest_nfv_plugin.tests.scenario.test_nfv_epa.TestBasicEpa.test_numamix_provider_network
  - tempest_nfv_plugin.tests.scenario.test_nfv_epa.TestBasicEpa.test_packages_compute
  - tempest_nfv_plugin.tests.scenario.test_nfv_dpdk_usecases.TestDpdkScenarios.test_min_queues_functionality
  - tempest_nfv_plugin.tests.scenario.test_nfv_dpdk_usecases.TestDpdkScenarios.test_equal_queues_functionality
  - tempest_nfv_plugin.tests.scenario.test_nfv_dpdk_usecases.TestDpdkScenarios.test_max_queues_functionality
  - tempest_nfv_plugin.tests.scenario.test_nfv_dpdk_usecases.TestDpdkScenarios.test_odd_queues_functionality
  - neutron_tempest_plugin.scenario.test_trunk.TrunkTest.test_trunk_subport_lifecycle
```

#### Tests configuration
**Note!** - For the tests configuration, refer to the tempest-nfv-plugin [documentation](https://github.com/redhat-openstack/tempest-nfv-plugin/tree/master/docs).

**Note!** - In case neutron tests should be run, add them exactly as nfv tests to the 'tempest_tests' list.
