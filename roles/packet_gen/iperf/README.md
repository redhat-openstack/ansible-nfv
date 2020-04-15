# NFV Performance -  iperf

## Description

Performs iperf benchmark between VMs wit in same and across different compute nodes.

## Playbook Variables

iperf_network: <network used for the testing>
iperf_lcores: <list of cpus used for iperf instances>

## Invocation

ansible-playbook playbooks/packet_gen/iperf/performance_scenario.yml -e cloud_resources=create --extra @/path/to/openstack_task_vars.yml

**NOTE:** Refer to roles/packet_gen/trex/README.md for additional information on cloud_resources.
