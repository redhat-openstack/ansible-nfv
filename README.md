# Ansible NFV playbooks


## Playbooks
* DPDK Role
    
    Set OVS+DPDK post install configuration on installed openstack environment.
    
    The playbook has been tested on the following network interface:
      - **Intel Corporation Ethernet 10G 2P X520 Adapter**


* SRIOV Role
    
    Set SRIOV post install configuration on installed openstack environment.
    
    The playbook has been tested on the following network interfaces:
      - **Intel Corporation Ethernet 10G 2P X520 Adapter**
      - **Broadcom Corporation NetXtreme II BCM57810 10 Gigabit Ethernet**


* CPU pinning, NUMA, Huge pages Role
    
    Set CPU pinning, NUMA and Huge pages configuration on installed openstack environment.
    
    The playbook can be merged with DPDK or SRIOV playbooks.


## Important
Please, modify the playbooks variables to meet your needs before running the playbooks.

For any question, refer to the NFV Cloud QE team - nfv-cloud-qe-team@redhat.com
