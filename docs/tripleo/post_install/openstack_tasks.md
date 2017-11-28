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
* Overcloud delete
    * Deletes the required stack.  
      Default stack is - 'overcloud'.
* Clear the environment
    * Delete keypair and instance.
      Default instance named - 'vm1'. 

By default, all the tasks runs one by one on the environment.  
The run could be separated by specifying tags of specific run.

## Role tags
* os_tasks - Default run. Executes all runs.
* setup_os_env - Run Openstack virtual env creation for env tasks.
* create_networks - Run networks creation.
* create_flavors - Run flavors creation.
* images_upload - Upload images to the Openstack environment.
* overcloud_delete - Delete the required overcloud stack.
* clear_env - Clears the environment by removing given instance and keypair.

## Run triggers
* setup_os_env - Executed if 'true'. True by default.
* create_networks - Executed if 'true'. True by default.
* create_flavors - Executed if 'true'. True by default
* images_upload - Executed if 'true'. True by default.
* overcloud_delete - Executed if 'true'. False by default.
* clear_env - Executed if 'true'. False by default.

## Role variables
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
  - name: private
    physical_network: tenant
    segmentation_id: 32
    cidr: 172.20.0.0/24
    router_name: router1
```

Set DNS servers.
```
dns_nameservers:
  - 8.8.8.8
  - 8.8.4.4
```

#### Flavors creation
Specify flavors that should be created.  
Flavor keys (property) value are optional.
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
    property:
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

***
The variables could be applied to the playbook run, by saving them into a separate yml file and include the file during the playbook execution.  
Note the '@' sign, which is used to apply the variables located within the provided file.

```
ansible-playbook playbooks/tripleo/post_install/openstack_tasks.yml -e @/path/to/the/variable/file.yml
```
