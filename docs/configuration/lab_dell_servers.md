# Lab Dell EMC Servers

## Description
The lab_dell_servers play performs the following server individual tasks:
- Query iDRAC information
- Performs a power action on server
- Sets device boot order

iDRAC 7/8 with Firmware version 2.40.40.40 or above and iDRAC 9 with Firmware version 3.00.00.00 are supported in this play
Will be used for iDRAC manipulation in automation jobs.  
**Note!** - Dell EMC iDRAC modules is shipped in this repo due to linting issues for now
**Note!** - No need in inventory file. The file is generated during the playbook execution.
**Note!** - Multiple iDRACs could be specified, passed as a yaml. See example at the bottom.
**Note!** - Some operations will reboot your servers without prompt.

* Query
    * Query iDRAC for hardware and software information
* Power Action
    * Perform power action on server
* Boot Order
    * Sets device boot order

## Run triggers
* verify_dependencies - Executed if 'true'. True by default.
* query_server - Executed if part of 'On', 'ForceOff', 'GracefulRestart', 'GracefulShutdown', 'PushPowerButton', 'Nmi' and not set to 'False', False by default.
* power_action - Executed if 'true'. False by default.
* set_boot_order - Executed if 'true'. False by default.

## Role variables
#### iDRAC details
- idrac_ip - iDRAC management IP/hostname.
- idrac_user - iDRAC user to authenticate with.
- idrac_pass - iDRAC user's password.
- idrac_port - iDRAC API port [Default: 443].

#### Dependency details
- verify_dependencies - Bool value which handles if dependencies should be resolved.

#### Query procedure
- query_server - Bool value which handles if iDRAC should be queried.

#### Power Action
- power_action - Value of the action to be performed on server.

#### Boot Order
- set_boot_order - Bool value which handles if boot order should be changed.
- boot_sequence - Value of boot sequence for servers to be set, if not defined will be equal to optimal_boot_sequence.
- optimal_boot_sequence - Value of optimal boot sequence used in NFV lab.

***
## Examples
The examples of running the playbook:  

```Installing dependencies:
ansible-playbook playbooks/configuration/lab_dell_servers.yml -e idrac_ip=['<idrac_ip>'] -e idrac_user='test' -e idrac_pass='pass' -e verify_dependencies=true
```

```Querying iDRAC:
ansible-playbook playbooks/configuration/lab_dell_servers.yml -e idrac_ip=['<idrac_ip>'] -e idrac_user='test' -e idrac_pass='pass' -e query_servers=true
```

```Power Action:
ansible-playbook playbooks/configuration/lab_dell_servers.yml -e idrac_ip=['<idrac_ip>'] -e idrac_user='test' -e idrac_pass='pass' -e power_action:'GracefulRestart'
```

```
# Using optimal boot sequence
ansible-playbook playbooks/configuration/lab_dell_servers.yml -e idrac_ip=['<idrac_ip>']' -e idrac_user='test' -e idrac_pass='pass' -e set_boot_order=true

# Using custom boot sequence
ansible-playbook playbooks/configuration/lab_dell_servers.yml -e idrac_ip=['<idrac_ip>']' -e idrac_user='test' -e idrac_pass='pass' -e set_boot_order=true -e boot_sequence='NIC.Integrated.1-1-1,NIC.Integrated.1-2-1'
```
