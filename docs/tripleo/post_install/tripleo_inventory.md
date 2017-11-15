# TripleO Inventory

## Description
From time to time, we may get a new Openstack environment for work/testing/etc.
In order to be able to run an Ansible playbooks or different ad-hoc commands against the overcloud nodes,
inventory file required.

TripleO Inventory play will generate new inventory file from the provided Undercloud host.  
The play could be run in two available scenarios:
1. The public key of your ssh key already located on the Undercloud host.  
   The play will generate three files:
  * inventory
  * ansible.ssh.config
  * id_rsa_overcloud

2. You have only the password of the Undercloud host.  
   The play will generate five files:
  * inventory
  * ansible.ssh.config
  * id_rsa_overcloud
  * id_rsa_undercloud
  * id_rsa_undercloud.pub


Inventory - Will hold the Undercloud node and all Overcloud nodes located within the environment.  
Ansible.ssh.config - SSH config file. Allow to connect to the overcloud nodes from the localhost.
```
For example:
ssh -F ansible.ssh.config controller-0
```
Id_rsa_overcloud - The ssh key for the connection to overcloud nodes. Used by the above files.  
Id_rsa_undercloud - In case, password provided to Undercloud host, play will generate new ssh key  
                    and will use it for the connection to Undercloud host.  
Id_rsa_undercloud.pub - Public key of the id_rsa_undercloud.

Each environment files will be generated under the following path:  
**{{ ansible_repo_dir }}/inventories/undercloud_name_env/**  
This provide the ability to have multiple environment inventories, and to choose the environment I want to work with.  
Each run, the latest generated environment will be symlinked to the **inventory** and **ansible.ssh.config** at the root of the ansible repo directory.

***

## Play variables
Provide the undercloud host.  
Mandatory variable.
```
host
```

Provide the user for the undercloud.  
Default user: 'stack'.  
Not mandatory variable.
```
user: stack
```

Specify the Undercloud ssh private key file.  
The public key should already be copied to the undercloud host.  
One of two parameters should be provided: ssh_key or ssh_pass.
```
ssh_key
```

Specify the password for the Undercloud host.
Use this variable in case there is no your public key on the Undercloud host.
One of two parameters should be provided: ssh_key or ssh_pass.
```
ssh_pass
```

Overcloud user. The user which has an access to the overcloud nodes.  
Default: 'heat-admin'.
```
overcloud_user: heat-admin
```

RC file path.
Default: '/home/stack/stackrc'.
```
rc_file_path
```

***
The example of running the TripleO Inventory playbook.  
With SSH key file:
```
ansible-playbook playbooks/tripleo/post_install/tripleo_inventory.yml -e host=undercloud-host-fqdn/ip -e ssh_key=/path/to/ssh/private/file
```

With password:
```
ansible-playbook playbooks/tripleo/post_install/tripleo_inventory.yml -e host=undercloud-host-fqdn/ip -e ssh_pass=undercloud_password
```
