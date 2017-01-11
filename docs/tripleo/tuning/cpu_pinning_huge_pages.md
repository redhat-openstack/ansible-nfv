# Cpu pinning and Huge pages configuration

## Description
The play sets CPU pinning and Huge pages configuration to the grub.  
By default, play runs on compute node, but could be overridden by providing the 'hosts' variable during the run.

The playbook could be combined with DPDK or SRIOV playbooks.

## Role variables
The variable provides the ability to change the target hosts that the playbook should run on. This variable is not required.  
Default value is - **compute**.
```
hosts: compute
```
> For example, run the role on "guest_vm1" instance:  
ansible-playbook playbooks/tripleo/tuning/cpu_pinning_huge_pages.yml -e hosts=guest_vm1 ...(additional role arguments)...

Sets the range of cpus that should be isolated.
```
cpu_pinning_cores: 3-8
```

Sets the size of the huge pages on the system.
```
hugepages_size: 1GB
```

Sets the count of the huge pages.
```
hugepages_count: 4
```
