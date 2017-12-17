# Ansible NFV playbooks
Ansible NFV repository holds various playbooks for installation, configuration, tuning, testing and day to day tasks related to NFV and Openstack.

## Documentation
For the repository documentation, refer to the **docs** directory, which provide explanation regarding the playbooks.  
In order to start working with TripleO environment, refer to the following doc - **docs/tripleo/post_install/tripleo_inventory.md**.  
The playbook will generate an inventory file for the tripleo environment.

**The minimum required version of Ansible for the playbooks >= 2.4**

## Playbooks
* TripleO
    * Tester
      * Tempest
      * Testpmd deploy and MoonGen run
      * Testpmd deploy and MoonGen run on secondary NUMA node
    * Tuning
      * CPU pinning and Huge pages
      * Tuned
    * Post install
      * Openstack tasks
      * Overcloud repo install
      * TripleO Inventory
* Moongen
    * Moongen install
    * Moongen run

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
