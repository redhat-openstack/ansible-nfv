# MoonGen

## Description
Runs Moongen application performance test by generating specified amount of packets.  
The results of the test, saved into the "/tmp/MoonGenOutput.txt" file on the Moongen server.  
More info could be found at:  
* https://github.com/emmericp/MoonGen
* https://www.net.in.tum.de/fileadmin/bibtex/publications/papers/MoonGen_IMC2015.pdf

## Role variables

Provide the startRate for Binaric search of packet generation.
```
startRate: 11
```

Provide the VLANs of your network providers.
```
vlan_id: 396
vlan_max_range: 400
```

Set to "true" in case of bi-directional test.
```
runBidirec: "true"
```

Set the length of searching and validation of every loop within the binaric search.
```
searchRunTime: 30
validationRunTime: 30
```

Acceptable loss of packets during the run.
```
acceptableLossPct: 0
```

Set the size of each frame
```
frameSize: 64
```

Set the ports which will be used for Rx/Tx(See note below).
```
ports: "{1,0}"
```

Provide the Dst and Src MAC addresses for SR-IOV use-cases.  
Provide only the Dst MAC of the VM for DPDK use-cases.  
```
srcMac: '{"a0:36:9f:22:e6:86", "a0:36:9f:22:e6:84"}'  
dstMac: '{"fa:16:3e:44:83:e9", "fa:16:3e:85:fd:14"}'
```

***
## Notes
* VlanIds and Ports should be syncronized with the  
  config of the nic port and vlan id on the Moongen side.  
  For example VLAN 396 should be allowed on the nic port 0.  
  The traffic from the nic port 0 on the Moongen will be  
  passed to the nic port 1 on the guest, and passed back  
  from the nic port 0 on the guest to the nic port 1  
  on the Moongen.  

* The variables could be applied to the playbook run, by saving them into a separate yml file and include the file during the playbook execution.  
  Note the '@' sign, which is used to apply the variables located within the provided file.

```
ansible-playbook playbooks/packet_gen/moongen/moongen-run.yml -e @/path/to/the/variable/file.yml
```
