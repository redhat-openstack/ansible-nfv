# NFV Lab Switches

## Description
The nfv_lab_switches play performs the following server individual tasks:
- Vlan configuration on the switch.
- Switch backup.
- Switch restore.  

Cisco and Juniper switches are supported by this play.  
Will be used for the switch manipulation in automation jobs.  
**Note!** - No need in inventory file. The file is generated during the playbook execution.
**Note!** - Multiple hosts and switches could be specified, separated by comma. See example at the bottom.

* Configure
    * Configure access port and vlan ID for the specified server based on the defined variables.
* Backup
    * Backup current cisco switch configuration.  
      The configuration saved under the role within the created directory named 'backup'.
* Restore
    * Restore provided configuration file to the switch.

## Run triggers
* config - Executed if 'true'. True by default.
* backup - Executed if 'true'. False by default.
* restore - Executed if 'true'. False by default.

## Role variables
#### Switch connection details
- cisco_ip - IP address of cisco switch.
- junos_ip - IP address of junos switch.
- switch_user - Username for the switch.
- switch_pass - Password for the switch.
```
cisco_ip: ''
junos_ip: ''
switch_user: ''
switch_pass: ''
```

#### Configuration details
- server_name - The name of the server that should be configured.  
  The name of the server defined the switch port number specified as variables.
- vlan_id - Vlan ID that should be configured for the server.
```
server_name: ''
vlan_id: ''
```

Example of the server/port configuration for the cisco switch:
```
tigon04:
  ports:
    - GigabitEthernet4/0/4
```

Example of the server/port configuration for the junos switch:
```
tigon01:
  ports:
    - xe-0/0/0
    - xe-0/0/1
```

#### Restore process
- configuration_file - Configuration file for restore task.
```
configuration_file: ''
```

***
## Examples
The examples of running the playbook:  
Configuration:
```
ansible-playbook playbooks/configuration/nfv_lab_switches.yml -e cisco_ip=<cisco_switch_ip/name> -e junos_ip=<junos_switch_ip/name> -e switch_user=<switch_user> -e switch_pass=<switch_pass> -e server_name=tigon04,tigon05 -e vlan_id=24
```

Backup:
```
ansible-playbook playbooks/configuration/nfv_lab_switches.yml -e cisco_ip=<cisco_switch_ip/name> -e junos_ip=<junos_switch_ip/name> -e switch_user=<switch_user> -e switch_pass=<switch_pass> -e config=false -e backup=true
```
**Note** - The backup file will be created within the roles/configuration/nfv_lab_switches/backup/ folder. If the folder does not exists, it will be created automatically.

Restore:
```
ansible-playbook playbooks/configuration/nfv_lab_switches.yml -e cisco_ip=<cisco_switch_ip/name> -e switch_user=<switch_user> -e switch_pass=<switch_pass> -e config=false -e restore=true -e configuration_file=<path_to_config_file>
```
