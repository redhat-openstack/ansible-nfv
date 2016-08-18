# Ansible NFV playbooks


## Playbooks

* DPDK Role
    
    Set OVS+DPDK post install configuration on installed openstack environment.
    
    The playbook has been tested on the following network interface:
      - **Intel Corporation Ethernet 10G 2P X520 Adapter**
* DPDK-second-nic role

    Configures OVS to use the second NIC, within a new bridge.

    Mostly used for MoonGens performance test.
     - **Intel Corporation Ethernet 10G 2P X520 Adapter

* SRIOV Role
    
    Set SRIOV post install configuration on installed openstack environment.
    
    The playbook has been tested on the following network interfaces:
      - **Intel Corporation Ethernet 10G 2P X520 Adapter**
      - **Broadcom Corporation NetXtreme II BCM57810 10 Gigabit Ethernet**


* CPU pinning, NUMA, Huge pages Role
    
    Set CPU pinning, NUMA and Huge pages configuration on installed openstack environment.
    
    The playbook can be merged with DPDK or SRIOV playbooks.

* Tuned Role

    The role sets and activates new tuned profile named cpu-partitioning, the profile sets the

    CPUAffinity using delivered Core-list


* Tempest Role

    Install and configure downstreams tempest with RHOS-NFV-QE tempest plugin.

    Specifying "port_vnic_type: True" value, the playbook configures the tempest.conf for SR-IOV test cases.

* Guest TestPMD Role

    Install and configure new venv at /root , creates 2 networks, new flavor and his keys and new image.

    The image starts TestPMD application automaticly, and have watchdog cron-every min, which checks the state of testpmd.service and tries to start it.


## Important
Please, modify the playbooks variables to meet your needs before running the playbooks.

For any question, refer to the NFV Cloud QE team - nfv-cloud-qe-team@redhat.com
