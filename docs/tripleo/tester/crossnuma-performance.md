# Tempest

## Description
Cross NUMA performance playbook will perform the following steps:
  - Delete running vm
  - Change vcpu_pin at /etc/nova/nova.conf (Part of workaround role)
  - Prepare the Compute host
  - Prepare the openstack environment
  - Configure the instance for performance
  - Run TestPMD application
  - Start performance measurement using MoonGen
  * This Play depend on "testpmd-deploy-run"! 

## Role tags
* setup_os_env - Run Openstack virtual env creation for env tasks.
* create_networks - Run networks creation.
* create_flavors - Run flavors creation.
* images_upload - Upload images to the Openstack environment.
* overcloud_delete - Delete the required overcloud stack.
* boot_instance - Create instance with components created above
* clear_env  - Clears the environment, delete the instance the their keypair


## Role variables
* Creation of networks
  At the example below; creation of 3 networks will be performed
  One external network, will be used as gateway for the router
  Two internal networks, named dpdk1-2, will be used for performance measurment.
```
networks:
  - name: external
    physical_network: dpdk_mgmt
    segmentation_id: 396
    external: true
    allocation_pool_start: 10.35.141.6
    allocation_pool_end: 10.35.141.10
    cidr: 10.35.141.0/28
    enable_dhcp: true
    gateway_ip: 10.35.141.14
    router_name: router

  - name: dpdk1
    physical_network: dpdk_data1
    segmentation_id: 502
    external: false
    allocation_pool_start: 10.10.102.100
    allocation_pool_end: 10.10.102.200
    cidr: 10.10.102.0/24
    enable_dhcp: true
    gateway_ip: 10.10.102.254
    router_name: router

  - name: dpdk2
    physical_network: dpdk_data2
    segmentation_id: 507
    external: false
    allocation_pool_start: 10.10.107.100
    allocation_pool_end: 10.10.107.200
    cidr: 10.10.107.0/24
    enable_dhcp: true
    gateway_ip: 10.10.107.254
    router_name: router
```
* Network type
```
network_type: vlan
```

* Instance creation, Please specify instances.
  - name - Must!
    flavor - Specify flavor, otherwise "nfv-flavor" will be taken by default.
    image - Specify image name, otherwise "centos" will be taken by default.
```
instances:
  - name: vm1
  - name: vm2
    image: rhel
    flavor: m1.medium
```

* Instance delete, Please specify instances.
  - name - Must!

```
instances:
  - name: vm1
  - name: vm2
```

* DNS name servers
```
dns_nameservers:
  - 8.8.8.8
  - 10.35.28.28
```

* Image for the guest[NOTE: have to be rhel/centos]
```
images:
  - name: centos7
    url: http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
```

* TestPMD version
```
version: v16.04
```

* Rhos release version which will be used on the guest.
  URL to latest rhos-relase.
```
rhos_version: 10
rhosurl: http://rhos-release.virt.bos.redhat.com/repos/rhos-release/rhos-release-latest.noarch.rpm
```

* Vlan IDs of internal network, will be used for performance.
```
vlan_id: 502
vlan_max_range: 507
```

* Source and dest MAC addresses for MoonGen application usage
  In case of DPDK, please specify the MAC addr of PORT1 at the MoonGen server
```
dstMac: '{"a0:36:9f:a9:a2:0e"}'
```

* The lcores of the intance to be tuned
```
isolated_cpus: 0,1,2,3
```

* MoonGen variables
```
startRate: 11
runBidirec: "true"
searchRunTime: 30
validationRunTime: 30
acceptableLossPct: 0
frameSize: 64
ports: "{0, 1}"
```
