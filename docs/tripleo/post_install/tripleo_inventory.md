# TripleO Inventory

## Description
TripleO Inventory play generates new inventory file from the provided Openstack TripleO environment.  
The play will generate two files:
  * inventory
  * ansible.ssh.config

Inventory - will hold the Undercloud node and all Overcloud nodes existing within the environment.  
Ansible.ssh.config - SSH config file. Allow to connect to the overcloud nodes from the localhost.
```
ssh -F ansible.ssh.config controller-0
```

**Requirement** - Before running the playbook, make sure to pass your public key to the undercloud.
```
ssh-copy-id -i /path/to/the/public/key stack@undercloud_server
```

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

Specify the undercloud ssh private key file.  
The public key should already be copied to the undercloud host.  
Mandatory variable.
```
ssh_file
```

Overcloud user. The user which has an access to the overcloud nodes.  
Default: 'heat-admin'.
```
overcloud_user: heat-admin
```

***
The example of running the TripleO Inventory playbook.
```
ansible-playbook playbooks/tripleo/post_install/tripleo_inventory.yml -e undercloud_host=undercloud-host-fqdn/ip -e ssh_file=/path/to/ssh/private/file
```
