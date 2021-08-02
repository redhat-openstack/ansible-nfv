# Ansible NFV playbooks
Ansible NFV repository holds various playbooks for installation, configuration, tuning, testing and day to day tasks related to NFV and Openstack.

## Documentation
Each role holds it's own documentation. Refer to the README.md file within the role.

**The minimum required version of Ansible for the playbooks >=2.9.0,<2.10.0**  
**Note** - In order to work properly with the selinux, make sure the **libselinux-python** package is installed on your host.

## Install
The ansible-nfv repository has a number of requirements that need to be installed within virtualenv.  
**For Production** - Install the packages by - `pip install -r requirements.txt`  
**For Development** - Install the packages by - `pip install -r test-requirements.txt`  

In addition to the above packages, ansible-nfv is using ansible collections.  
Required collections defined within the **requirements.yaml** file.  
Install the collections in addition to the above commands - `ansible-galaxy collection install -r requirements.yaml`

## How to contribute
Refer to the `contribution.md` guide.

## Note
Please, modify the playbooks variables to meet your needs before running the playbooks.

The variables could be applied to the playbook run, by saving them into a separate yml file and include the file during the playbook execution.  
Note the '@' sign, which is used to apply the variables located within the provided file.

```
ansible-playbook playbooks/path/to/the/playbook.yml -e @/path/to/the/variable/file.yml
```

For any question, refer to the NFV Cloud QE team - nfv-cloud-qe-team@redhat.com
