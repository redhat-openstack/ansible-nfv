# Openstack tasks

## Description
The `openstack tasks` role performs the following tasks on the existing Openstack environment.

* Setup Openstack environment
    * Creates and prepares the virtual pip environment with all required command line tools.  
      Creates clouds.yml file with all the details for the connection to the Openstack env.
* Creates users, projects, clouds.yaml user configs.
    * Creates users and projects based on the specified variables.
    * Generates users rc files.
    * Generates users configs within the clouds.yaml file for the later tasks by the users.
* Creates quota
    * Creates quota for a project such as number of cpu's cores, ram, instances.
* Creates networks
    * Creates networks, subnets, routers and ports by using the variables list provided to the play.  
      Public networks sets as a gateway on the router and private networks sets as a router interface by using the 'external' flag within the variables provided.  
      The interfaces for the instance could be specified as a network name or as a created port name.
      Each networks should be added to cloud_name, tenant user, admin, called overcloud
* Upload images and set image properties
    * Upload provided images to the glance store of the overcloud. Properties can set if required.
* Aggregate groups
    * Creates aggregation groups with defined hosts and metadata.  
      **NOTE** - a must configuration is required: enable "AggregateInstanceExtraSpecsFilter"  
      in a /etc/nova/nova.conf file (controllers nodes) to the scheduler_default_filters defenition.
* Creates flavors and extra_specs
    * Creates flavors for the instances. Extra_specs could be created for the flavors if required.
* Creates keypair
    * Creates keypair and fetch the file to the client.
      Each keypair should be added to cloud_name
* Creates security groups
    * Creates security groups with defined protocols.
      Each security group should be added to cloud_name
* Boot an instance(s)
    * Boot the defined instances on the overcloud.
      Each instance should be added to cloud_name
* Overcloud delete
    * Deletes the required stack.  
      Default stack is - 'overcloud'.
* Resources output file generation
    * Generates yaml resources file with instances and keypair details.

By default, all the tasks runs one by one on the environment.  
The run could be separated by specifying tags of specific run.

## Role tags
* setup_os_env - Run Openstack virtual env creation for env tasks.
* user - Run users and projects creation and.
* quota - Run quota creation.
* network - Run networks creation.
* net_port - Run instance port creation.
* aggregate - Run group aggregate creation.
* flavor - Run flavors creation.
* image - Upload images to the Openstack environment.
* keypair - Run keypair creation.
* security_group - Run security groups creation.
* instance - Boot defined instances.
* overcloud_delete - Delete the required overcloud stack.
* resources_output - Generate instance and keypair details yaml file.

## Run triggers
* setup_os_env - Executed if 'true'. True by default.
* user - Executed if 'true'. False by default.
* quota - Executed if 'true'. False by default.
* network - Executed if 'true'. True by default.
* net_port - Executed if 'true'. True be default.
* aggregate - Executed if 'true'. False by default.
* flavor - Executed if 'true'. True by default.
* image - Executed if 'true'. True by default.
* keypair - Executed if 'true'. True by default.
* security_group - Executed if 'true'. True by default.
* instance - Executed if 'true'. False by default.
* overcloud_delete - Executed if 'true'. False by default.
* resources_output - Executed if 'true'. False by default.
**NOTE:** Currently os_floating_ip module doesn't return FIP in a consistent matter when an instance contains multiple NICs
* resource_generate_inventory - Add generated instances to dynamic Ansible inventory

**Sample file:**  
For the sample file, refer to the following [link](openstack_tasks_config_sample.yml).

**Multiple network interfaces configuration:**  
For the multiple network interfaces configuration, refer to the [explanation](openstack_instance_net_config.md).

## Role default variables
#### State of the resource
The state could be 'present' or 'absent'.
```
resource_state: present
```

#### The name of the "cloud", the tasks should be run on.
The "cloud" represents a stack (undercloud/overcloud), or a user that the playbook should interact with.  
All "clouds" configuration resides within the "~/.config/openstack/clouds.yaml" file.  
A different cloud name could be set on each resource.  
As a result multiple users resources could be created at a single playbook run.
```
cloud_name: overcloud
```

#### The path to the clouds.yaml file.
```
clouds_yaml_file_path: ~/.config/openstack/clouds.yaml
```

#### List of users and projects that should be created
#### Quotas could be defined for a user if needed.
```
users:
  - name: test_user1
    pass: 12345678
    project: test_project1
    domain: default
    role: member
    quota:
      - cores: 20
        ram: 20480
        instances: 25
  - name: test_user2
    pass: 87654321
    project: test_project2
    domain: default
    role: member
```

#### Network creation variables
Define the networks that should be created on the overcloud.
- 'name' - The name of the network. Required.
- 'physical_network' - The physnet of the network. Not required.
- 'segmentation_id' - The VLAN ID of the network. Not required.
- 'network_type' - Allowed values are: vlan/vxlan/flat. Not required.
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
    cloud_name: overcloud
    physical_network: public
    segmentation_id: 25
    network_type: vlan
    allocation_pool_start: 10.0.0.12
    allocation_pool_end: 10.0.0.100
    cidr: 10.0.0.0/24
    enable_dhcp: false
    gateway_ip: 10.0.0.254
    external: true   # The "external: true" with "router_name" adds the network as the default gateway.
    router_name: router1
    shared: true
  - name: private1
    physical_network: tenant1
    segmentation_id: 32
    cidr: 172.20.0.0/24
    external: false   # The "external: false" with the "router_name" sets the network as an interface for the router.
    router_name: router1
  - name: private2
    cloud_name: nfv_user 
    physical_network: tenant2
    cidr: 173.30.0.0/24
    external: false
    router_name: router1
    cloud_name: nfv_user 
  - name: private3
    physical_network: tenant3
    cidr: 174.40.0.0/24
```

Set DNS servers.
```
dns_nameservers:
  - 8.8.8.8
  - 8.8.4.4
```

#### Aggregate groups creation
Specify the aggregation groups that should be created.
```
aggregate_groups:
  - name: TREX_AG
    hosts:
      - compute-0.localdomain
      - compute-1.localdomain
    metadata:
      - flavor=trex_ag
        flavor=dut_ag
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
      "hw:mem_page_size": "1GB"
      "hw:numa_mem.0": "4096"
      "hw:numa_nodes": "1"
      "hw:numa_cpus.0": "0,1,2,3"
      "hw:cpu_policy": "dedicated"
      # Configure metadata of the created aggregation group as a flavor extra specs
      in order to initially boot an instance on a preferred hypervisor.
      "aggregate_instance_extra_specs:flavor": "trex_ag"
```

#### Images upload variables
Default images to upload
Image properties value are optional.
```
images:
  - name: cirros
    url: http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img

  - name: multiqueue
    url: http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
    properties:
      hw_vif_multiqueue_enabled: "true"
```
Local images on undercloud can also be used, by using the file URI scheme.
```
images:
  - name: centos7cloud
    url: file:///tmp/CentOS-7-x86_64-GenericCloud.qcow2
```

#### Keypairs names list
Keypairs to be created.  
The private key fetched to the client local.
```
keypairs:
  - name: test_keypair
    cloud_name: overcloud
```

#### Security groups
Specify the security groups and rules that should be created.
```
security_groups:
  - name: test_secgroup
    cloud_name: overcloud
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

#### User Data
Specify global userdata content to be passed via metadata server to cloud-init.
The global userdata could be used in case it is similar for all the instances.
The userdata could be overridden by passing it to specific instance.
```
global_userdata: |
  users:
  - name: cloud-init
    lock-passwd: false
    passwd: password
```

#### Instances
Specify the instance and arguments that the instance should be created with.
```
instances:
  - name: vm1
    cloud_name: overcloud
    groups:        # Instance could be attached to multiple groups. The groups will be created as inventory groups.
      - vm_group1
      - vm_group2
    flavor: nfv_flavor
    image: centos
    key_name: test_keypair
    sec_groups: test_secgroup
    # Assigning FIP address to an instance, choose 'ext_net' as your routable network
    and 'int_net' as an internal NATed network that the FIP address will be assigned to it
    floating_ip:
      ext_net: public
      int_net: private_net3
    # NICs to be attached to instance, must be present or created by `net_ports`
    nics:
      - port-name=private_net1_port1
      - port-name=private_net2_port2
      - net-name=private_net3
    # Pass userdata to the instance
    userdata: |
      #cloud-config
      user: root
      password: 123456
    # Optional, Specify if nova should attach metadata content via CD-ROM to instance
    config_drive: True
    # Ports to be created, which can be attached to instance using `nics`
    net_ports:
      - name: private_net1_port1
        network: private_net1
        type: normal
        sec_groups: test_secgroup
      - name: private_net2_port2
        network: private_net2
        type: direct
  - name: vm2
    connection_user: user     # The variable could be omitted
    flavor: nfv_flavor
    image: centos
    key_name: test_keypair
    sec_groups: test_secgroup
    floating_ip:
      ext_net: public
      int_net: private_net3
    nics:
      - net-name=private_net3
      - port-name=private_net1_port3
    net_ports:
      - name: private_net1_port3
        network: private_net1
        type: normal
        sec_groups: test_secgroup
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

The path to the file output of the created resources.
Will contain booted instances and keypair details.  
Example of usage: Could be used by the tempest in order to execute the tests  
on already provisioned resources.
```
resources_output_file: /home/stack/resources_output_file.yml
```

Generate a dynamic Ansible inventory based on resources created.  
**NOTE:** As of now, it's broken due to `os_floating_ip` module not being consistent when an instance contains multiple NICs. Please refer to [Dynamic Host Inventory Role](../tripleo_inventory/README.md) for a workaround.
Default is - **False**
```
resource_generate_inventory: False
```

***
The variables could be applied to the playbook run, by saving them into a separate yml file and include the file during the playbook execution.  
Note the '@' sign, which is used to apply the variables located within the provided file.

```
ansible-playbook playbooks/tripleo/post_install/openstack_tasks.yml -e @/path/to/the/variable/file.yml
```
