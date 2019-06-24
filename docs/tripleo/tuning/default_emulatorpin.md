# Default emulatorpin configuration on DUT instances

## Description
Following play sets the default shared cpu emulatorpin on the DUT instances.  

## Role variables
The variable provides the ability to change the target hosts that the playbook should run on. This variable is required.  
```
dut_compute: compute-1
```

Sets the range of shared cpus that should be set to the emulatorpin.
```
cpu_list: '0,20,1,21'
```
