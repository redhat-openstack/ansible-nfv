# Ansible NFV playbooks
Ansible NFV repository holds various playbooks for installation, configuration, tuning, testing and day to day tasks related to NFV and Openstack.

## Documentation
For the repository documentation, refer to the **docs** directory, which provide explanation regarding the playbooks.

## Playbooks
* TripleO
    * Tester
      * Tempest
    * Tuning
      * CPU pinning and Huge pages
      * Tuned
    * DPDK
    * Openstack tasks
    * Overcloud repo install
    * SRIOV
* Moongen
    * Moongen install
    * Moongen run
* Packstack
    * Tester
      * Guest Testpmd
      * Tempest
      * Testpmd install
    * Tuning
      * CPU pinning and Huge pages
      * Tuned
    * DPDK
    * Openstack tasks
    * SRIOV

## How to contribue
Patches should be submitted using git review to the GerritHub.

## Important
Please, modify the playbooks variables to meet your needs before running the playbooks.

For any question, refer to the NFV Cloud QE team - nfv-cloud-qe-team@redhat.com
