# Ansible NFV playbooks
Ansible NFV repository holds various playbooks for installation, configuration, tuning, testing and day to day tasks related to NFV and Openstack.

## Documentation
For the repository documentation, refer to the **docs** directory, which provide explanation regarding the playbooks.

## Playbooks
* TripleO
    * NFV
      * DPDK
      * SRIOV
    * Tester
      * Tempest
    * Tuning
      * CPU pinning and Huge pages
      * Tuned
    * Post install
      * Openstack tasks
      * Overcloud repo install
* Moongen
    * Moongen install
    * Moongen run
* Packstack
    * NFV
      * DPDK
      * SRIOV
    * Tester
      * Guest Testpmd
      * Tempest
      * Testpmd install
    * Tuning
      * CPU pinning and Huge pages
      * Tuned
    * Post install
      * Openstack tasks

## How to contribue
Patches should be submitted using git review to the GerritHub.

## Note
Please, modify the playbooks variables to meet your needs before running the playbooks.

The variables could be applied to the playbook run, by saving them into a separate yml file and include the file during the playbook execution.  
Note the '@' sign, which is used to apply the variables located within the provided file.

```
ansible-playbook playbooks/path/to/the/playbook.yml -e @/path/to/the/variable/file.yml
```

For any question, refer to the NFV Cloud QE team - nfv-cloud-qe-team@redhat.com
