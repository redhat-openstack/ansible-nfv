# Molecule for **collect_ovs_configs** role

## Overview
The test process of the **collect_ovs_configs** role requires functional OpenStack environment  
as the role needs an access to a working openvswitch package.  
The `tripleo_inventory` role will be used as a prepare step to create the inventory for the existing env.  

## Install
For the testing of current role, delegated driver is used.  
Use test-requirements.txt file in the root of the repo in order to install molecule and its components.

```
$ pip install -r test-requirements.txt
```

## Execution
Current testing scenario requires to provide environment variables.
* TEST_HOST - The host name of the environment hypervisor or undercloud (depend on the type of the environment).
* TEST_SSH_KEY - The ssh key to connect to the test host.
* TEST_ENV_TYPE - Optional. The type of the environment - virt / hybrid / baremetal. By default - virt.

Molecule full testing cycle could be started by executing the following command command:
```
$ TEST_HOST=hypervisor_name TEST_SSH_KEY=/path/to/hypervisor/ssh/key molecule test
```

The scenario will perform the following test steps:
- lint
- syntax
- prepare
- destroy
- converge
- verify
- destroy
- cleanup
