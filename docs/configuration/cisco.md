# Cisco

## Description
Cisco play performs server individual vlan configuration on the switch.  
Will be used for the switch manipulation in automation jobs.  
**Note!** - No need in inventory file. The file is generated during the playbook execution.
**Note!** - Multiple hosts could be specified, separated by comma. See example at the bottom.

* Configure
    * Configure access port and vlan ID for the specified server based on the defined variables.
* Backup
    * Backup current cisco switch configuration.  
      The configuration saved under the cisco role within the created backup directory.
* Restore
    * Restore provided configuration file on the cisco switch.

## Run triggers
* config - Executed if 'true'. True by default.
* backup - Executed if 'true'. False by default.
* restore - Executed if 'true'. False by default.

## Role variables
#### Switch connection details
- switch_ip - IP address of cisco switch.
- switch_user - Username of cisco switch.
- switch_pass - Password of cisco switch.
```
switch_ip: ''
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

Example of the server/port configuration:
```
tigon04:
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
The example of running the cisco playbook:  
Configuration:
```
ansible-playbook playbooks/configuration/cisco.yml -e switch_ip=<switch_ip> -e switch_user=<switch_user> -e switch_pass=<switch_pass> -e server_name=tigon04,tigon05 -e vlan_id=24
```

Backup:
```
ansible-playbook playbooks/configuration/cisco.yml -e switch_ip=<switch_ip> -e switch_user=<switch_user> -e switch_pass=<switch_pass> -e config=false -e backup=true
```
**Note** - The backup file will be created within the roles/configuration/cisco/backup/ folder. If the folder does not exists, it will be created automatically.

Restore:
```
ansible-playbook playbooks/configuration/cisco.yml -e switch_ip=<switch_ip> -e switch_user=<switch_user> -e switch_pass=<switch_pass> -e config=false -e restore=true -e configuration_file=<path_to_config_file>
```
