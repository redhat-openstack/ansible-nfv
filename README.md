# Ansible NFV playbooks
Ansible NFV repository holds various playbooks for installation, configuration, tuning, testing and day to day tasks related to NFV and Openstack.

## Documentation
Each role holds it's own documentation. Refer to the README.md file within the role.

**The minimum required version of Ansible for the playbooks >=2.7.5,<2.8.0**  
**Note** - In order to work properly with the selinux, make sure the **libselinux-python** package is installed on your host.

## How to contribue
Refer to the `contribution.md` guide.

## Note
Please, modify the playbooks variables to meet your needs before running the playbooks.

The variables could be applied to the playbook run, by saving them into a separate yml file and include the file during the playbook execution.  
Note the '@' sign, which is used to apply the variables located within the provided file.

```
ansible-playbook playbooks/path/to/the/playbook.yml -e @/path/to/the/variable/file.yml
```

For any question, refer to the NFV Cloud QE team - nfv-cloud-qe-team@redhat.com
