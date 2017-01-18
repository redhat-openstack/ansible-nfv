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

By default, all the tasks runs one by one on the environment.  
The run could be separated by specifying tags of specific run.

## Role tags
* os_tasks - Default run. Executes all runs.
* setup_os_env - Run Openstack virtual env creation for env tasks.
* create_networks - Run networks creation.
* images_upload - Upload images to the Openstack environment.
* overcloud_delete - Delete the required overcloud stack.

## Run triggers
* setup_os_env - Executed if 'true'. True by default.
* create_networks - Executed if 'true'. True by default.
* images_upload - Executed if 'true'. True by default.
* overcloud_delete - Executed if 'true'. False by default.

## Role variables
#### Network creation variables
Define the networks that should be created on the overcloud.  
'External: true' value could be defined just for the external network.  
Allocation pools could be defined as an option in case specific pool range should be defined.  
Otherwise, pool will be calculated by 'cidr' value.
```
networks:
  - name: public
    physical_network: public
    segmentation_id: 25
    external: true
    allocation_pool_start: 10.0.0.12
    allocation_pool_end: 10.0.0.100
    cidr: 10.0.0.0/24
    enable_dhcp: false
    gateway_ip: 10.0.0.254
    router_name: router1
  - name: private
    physical_network: tenant
    segmentation_id: 32
    cidr: 172.20.0.0/24
    enable_dhcp: true
    gateway_ip: 172.10.0.254
    router_name: router1
```

Set the network type. Available values: vlan, vxlan.
```
network_type: vlan
```

Set DNS servers.
```
dns_nameservers:
  - 8.8.8.8
  - 8.8.4.4
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
