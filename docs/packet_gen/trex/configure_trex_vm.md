# Trex

## Description
Configures Trex on specified host.

**NOTE** Automatic discovery is limited to two ports assigned to Trex, above that you must supply external configuration

## Role Variables
### Trex Instance Variables
Trex guest instance name or UUID to be used in API queries
```
trex_server: 'trex'
```

Trex public mangement IP address which can be used to access the instance
```
trex_server_mgmt_ip: "10.11.12.13"
```

Attempt to discover floating IP using OpenStack APIs if 'trex_server_mgmt_ip' is empty
```
discover_instance_external_ip: True
```

Trex user credentials used to login into an instance, can be accessed via username+password or username+ssh_key
```
trex_server_user: 'root' # Username used to log in
trex_server_password: '12345678' # Password used to log in
trex_ssh_key: '/path/to/keys' # SSH key used to log in
trex_ssh_pass: 'ssh_secret' # SSH Secret
```

### Trex Configuration Variables

States if config variables are parsed externally
```
trex_conf_file: True
```

Trex configuration parameters
```
trex_port_info: ['52:54:00:00:00', '52:54:00:00:00'] # Trex ports' MAC addresses
trex_cfg_version: 2 # Trex config version
trex_interfaces: ['00:03.0', '00:04.0'] # Trex interfaces PCI slots
trex_platform: # Additional Platform specific configuration/tuning
    master_thread_id: 2
    latency_thread_id: 3
    dual_if:
      - socket: 0
        threads: [4,5,6,7,8,9,10,11]
```

## Example
Examples of running this playbook:

Run configuration and attempt to parse everything during run time
```
ansible-playbook playbooks/packet_gen/trex/configure_trex_vm.yml -e trex_server=trex
```

Run configuration and attempt to parse NICs data from predefined ip address
```
ansible-playbook playbooks/packet_gen/trex/configure_trex_vm.yml -e trex_server=trex -e trex_server_mgmt_ip 1.2.3.4
```

run configuration with external values from external config file
```
ansible-playbook playbooks/packet_gen/trex/configure_trex_vm.yml -e trex_server=trex -e trex_conf_file=true -e @/path/to/config_vars.yaml
```
