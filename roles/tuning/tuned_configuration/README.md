# Tuned

## Description
Installation, configuration and activation of Tuned CPU-partitioning profile.  
The profile sets the CPUAffinity using delivered CPU cores list.

## Role variables
Provide repositories which has tuned and tuned profile packages.
```
repos:
  - name:
    url:
  - name:
    url:
```

Provide CPU cores for the cpu isolation.
```
isolated_cores: 4,6,8,10,12,14
```

***
The variables could be applied to the playbook run, by saving them into a separate yml file and include the file during the playbook execution.  
Note the '@' sign, which is used to apply the variables located within the provided file.

```
ansible-playbook playbooks/tripleo/tuning/tuned.yml -e @/path/to/the/variable/file.yml
```
