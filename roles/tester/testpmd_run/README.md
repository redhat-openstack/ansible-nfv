# TestPMD run

## Description
Configure and execute TestPMD application.
**Note** - This role depends on the `testpmd_install`.

## Role variables
Vlan IDs of internal network, will be used for performance.
```
vlan_id: 502
vlan_max_range: 507
```

Source and dest MAC addresses for MoonGen application usage
In case of DPDK, please specify the MAC addr of PORT1 at the MoonGen server
```
dstMac: '{"a0:36:9f:a9:a2:0e"}'
```

The lcores of the intance to be tuned
```
isolated_cpus: 0,1,2,3
```

MoonGen variables
```
startRate: 11
runBidirec: "true"
searchRunTime: 30
validationRunTime: 30
acceptableLossPct: 0
frameSize: 64
ports: "{0, 1}"
```
