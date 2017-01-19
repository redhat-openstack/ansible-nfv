# MoonGen

## Description
Installation and configuration of MoonGen application over selected server.
The playbook binds the relevant NICs using 'vfio_pci' module, allocate Huge-Pages and builds the application.

## Role variables
### MoonGen variables
```

Provide CPU cores for MoonGen application and cpu isolation.
```
vcpu_pin: 2,4,6,8,10,12,14,16,18,20,22,24,26,28,30
```

Provide the Huge-pages size and amount for MoonGen usage.
```
hugepages_size: 1GB
hugepages_count: 20
```

Provide The NIC names to be bind to MoonGen app.
```
dpdk_nic_name: enp6s0f0
dpdk_second_nic_name: enp6s0f1
```

Set the number of memory channels[Default of servers is '4', see https://en.wikipedia.org/wiki/Multi-channel_memory_architecture for more info]
```
memory_channels: 4
```

Specify the socket memory allocation, corresponding to EAL argument "--socket-mem", first argument for NUMA-0 second to NUMA-1.
```
socketmem: "2048,2048"
```

Provide the url of MoonGen Github.
```
moongen_url: https://github.com/atheurer/MoonGen.git
```

***
The variables could be applied to the playbook run, by saving them into a separate yml file and include the file during the playbook execution.  
Note the '@' sign, which is used to apply the variables located within the provided file.

```
ansible-playbook playbooks/tripleo/tuning/tuned.yml -e @/path/to/the/variable/file.yml
```
