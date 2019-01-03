# Openstack tasks

## Description
Openstack tasks play perform the following tasks on the existing Openstack environment.

* Setup Openstack environment
    * Creates and prepares the virtual pip environment with all required command line tools.  
      Creates clouds.yml file with all the details for the connection to the Openstack env.
* Creates networks
    * Creates networks, subnets and routers by using the variables list provided to the play.  
      Public networks sets as a gateway on the router and private networks sets as a router interface by using the 'external' flag within the variables provided.
* Upload images
    * Upload provided images to the glance store of the overcloud.
* Creates flavors and extra_specs
    * Creates flavors for the instances. Extra_specs could be created for the flavors if required.
* Creates keypair
    * Creates keypair and fetch the file to the client.
* Creates security groups
    * Creates security groups with defined protocols.
* Boot an instance(s)
    * Boot the defined instances on the overcloud.
* Overcloud delete
    * Deletes the required stack.  
      Default stack is - 'overcloud'.
* Data file generation
    * Generates yaml data file with instances and keypair details.

By default, all the tasks runs one by one on the environment.  
The run could be separated by specifying tags of specific run.

## Role tags
* setup_os_env - Run Openstack virtual env creation for env tasks.
* network - Run networks creation.
* flavor - Run flavors creation.
* image - Upload images to the Openstack environment.
* keypair - Run keypair creation.
* security_group - Run security groups creation.
* instance - Boot defined instances.
* overcloud_delete - Delete the required overcloud stack.
* data_file - Generate instance and keypair details yaml file.

## Run triggers
* setup_os_env - Executed if 'true'. True by default.
* network - Executed if 'true'. True by default.
* flavor - Executed if 'true'. True by default.
* image - Executed if 'true'. True by default.
* keypair - Executed if 'true'. True by default.
* security_group - Executed if 'true'. True by default.
* instance - Executed if 'true'. False by default.
* overcloud_delete - Executed if 'true'. False by default.
* data_file - Executed if 'true'. False by default.

## Role default variables
#### State of the resource
The state could be 'present' or 'absent'.
```
resource_state: present
```

#### The name of the overcloud/user, the tasks should be run on.
```
overcloud_name: overcloud
```

#### Network creation variables
Define the networks that should be created on the overcloud.
- 'name' - The name of the network. Required.
- 'physical_network' - The physnet of the network. Not required.
- 'segmentation_id' - The VLAN ID of the network. Not required.
- 'network_type' - Allowed values are: vlan/vxlan. Default is - vlan. Not required.
- 'External: true' - Value could be defined just for the external network. Not required.
- 'allocation_pool_start/end' - Could be defined as an option in case specific pool range should be defined.  
  Otherwise, pool will be calculated by 'cidr' value. Not required.
- 'cidr' - The CIDR of the network. Required.
- 'enable_dhcp' - Set the dhcp state. Default is - enabled. Not required.
- 'gateway_ip' - Define specific gateway ip address if needed. Default is the first ip of the pool. Not required.
- 'router_name' - The name of the router. Required.
- 'shared' - Define whether this network is shared or not. Not required.
```
networks:
  - name: public
    physical_network: public
    segmentation_id: 25
    network_type: vlan
    external: true
    allocation_pool_start: 10.0.0.12
    allocation_pool_end: 10.0.0.100
    cidr: 10.0.0.0/24
    enable_dhcp: false
    gateway_ip: 10.0.0.254
    router_name: router1
    shared: true
  - name: private1
    physical_network: tenant1
    segmentation_id: 32
    cidr: 172.20.0.0/24
    router_name: router1
  - name: private2
    physical_network: tenant2
    cidr: 173.30.0.0/24
```

Set DNS servers.
```
dns_nameservers:
  - 8.8.8.8
  - 8.8.4.4
```

#### Flavors creation
Specify flavors that should be created.  
Flavor keys (extra_specs) value are optional.
```
flavors:
  - name: m1.medium
    ram: 2048
    disk: 20
    vcpus: 2

  - name: nfv-flavor
    ram: 4096
    disk: 20
    vcpus: 4
    extra_specs:
      - "hw:mem_page_size": "1GB"
        "hw:numa_mem.0": "4096"
        "hw:numa_nodes": "1"
        "hw:numa_cpus.0": "0,1,2,3"
        "hw:cpu_policy": "dedicated"
```

#### Images upload variables
Default images to upload
```
images:
  - name: cirros
    url: http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
```

#### Keypair name
Keypair to be created.  
The private key fetched to the client local.
```
keypair_name: test_keypair
```

#### Security groups
Specify the security groups and rules that should be created.
```
security_groups:
  - name: test_secgroup
    rules:
      - protocol: icmp
        port_range_min: -1
        port_range_max: -1
        remote_ip_prefix: 0.0.0.0/0
      - protocol: tcp
        port_range_min: 22
        port_range_max: 22
        remote_ip_prefix: 0.0.0.0/0
```

#### Instances
Specify the instance and arguments that the instance should be created with.
```
instances:
  - name: vm1
    flavor: nfv_flavor
    image: centos
    key_name: "{{ keypair_name }}"
    sec_groups: test_secgroup
    nics: net-name=private1,net-name=private2
    floating_ip: yes
```

#### Overcloud delete variables
Rc file path for the access to the stack.  
Default is - **/home/stack/stackrc**
```
rc_file_path: /home/stack/stackrc
```

The name of the overcloud that should be deleted.  
Default is - **overcloud**
```
overcloud_name: overcloud
```

The file location of client pem file on remote host  
Default is - None
```
client_ca_cert: /path/to/the/file
```

Path of  the data yaml file to generate.  
Will contain booted instances and keypair details.  
Example of usage: Could be used by the tempest in order to execute the tests  
on already provisioned resources.
```
data_file_path: /home/stack/data.yml
```

***
The variables could be applied to the playbook run, by saving them into a separate yml file and include the file during the playbook execution.  
Note the '@' sign, which is used to apply the variables located within the provided file.

```
ansible-playbook playbooks/tripleo/post_install/openstack_tasks.yml -e @/path/to/the/variable/file.yml
```
