# TripleO Inventory

## Description
TripleO Inventory play will generate a new inventory file from the provided Undercloud/Hypervisor host.

From time to time, we may get an already installed Openstack environment for work/testing/etc.
In order to be able to run an Ansible playbooks or different ad-hoc commands against the overcloud nodes,
inventory file is required.

## Structure
At the end of the play the following structure will appear:
```
|-> inventory file (soft link to the last environment)
|-> ansible.ssh.config (soft link to the last environment)
|
|-> environments
    |
    |-> First environment
    |     |-> inventory file
    |     |-> ansible.ssh.config file
    |     |-> ssh keys
    |
    |-> Second environment
    |     |-> inventory file
    |     |-> ansible.ssh.config file
    |     |-> ssh keys
```
**Note!** - Each run, the latest generated environment will be symlink to the **inventory** and **ansible.ssh.config** at the root of the ansible repo directory.

## Supported environment types:
The play adapted to the baremetal, hybrid or virt environment.  
**Baremetal** - Undercloud and Overcloud nodes (Controllers, Computes, etc...) are fully baremetal.  
**Hybrid** - Undercloud and Controllers nodes are virtual (Resides on a single host) and the Computes are baremetal.  
**Virt** - Undercloud and Overcloud nodes (Controllers, Computes, etc...) are virtual and resides on a single machine.

**Note!** - For baremetal environment add ```-e setup_type=baremetal```, and for virt or hybrid environment add ```-e setup_type=virt```

The play could be run in two available scenarios:
1. The public key of your ssh key already located on the Undercloud/Hypervisor host.  
   The play will generate three files:
  * inventory
  * ansible.ssh.config
  * id_rsa_overcloud

2. You have only the password of the Undercloud/Hypervisor host.  
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

***
## Play variables
Provide the type of the environment.  
Default: 'baremetal'  
Mandatory variable.
```
setup_type
```

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

Define custom undercloud user if required.  
By default the variable is not used.  
Default value is - stack.
```
custom_undercloud_user
```

Undercloud could be used for various tasks like tester or something else.  
The tasks could use inventory groups.  
Define the groups, Undercloud host should be added to.  
Multiple groups should be separated by the comma.
```
undercloud_groups: undercloud,tester
```

***
## Examples
The example of running the TripleO Inventory playbook.  
With SSH key file for baremetal environment:
```
ansible-playbook playbooks/tripleo/post_install/tripleo_inventory.yml -e host=undercloud-host-fqdn/ip -e ssh_key=/path/to/ssh/private/file -e setup_type=baremetal
```
With SSH key file for hybrid or virt environment:
```
ansible-playbook playbooks/tripleo/post_install/tripleo_inventory.yml -e host=undercloud-host-fqdn/ip -e user=root -e ssh_key=/path/to/ssh/private/file -e setup_type=virt
```

With password:
```
ansible-playbook playbooks/tripleo/post_install/tripleo_inventory.yml -e host=undercloud-host-fqdn/ip -e user=root -e ssh_pass=undercloud_password
```
