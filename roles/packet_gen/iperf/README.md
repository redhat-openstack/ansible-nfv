# NFV Performance -  iperf

## Description

Performs iperf benchmark between VMs with in same and across different compute nodes.

In current implementation of this test suite, it is assumed that, only two compute nodes are chosen for the test. In these two nodes, the first node (i.e dut_group[0]) is chosen for iperf server instance. The second node is chosen for iperf client instance, hence able to perform test for "inter-compute" nodes. For "intra-compute" nodes test, another iperf client instance is launched within same node where iperf server is running (i.e first node). There is no hosts aggregation or zone configured, hence it is assumed that, order of scheduling compute nodes for iperf server, iperf client (inter-compute) and iperf client (intra-compute) go in sequential and round-robin order so that, dut_group[0], dut_group[1], dut_group[2] instances point to the iperf instances.

## Playbook Variables

iperf_network: <network used for the testing>
iperf_lcores: <list of cpus used for iperf instances>

## Invocation

ansible-playbook playbooks/packet_gen/iperf/performance_scenario.yml -e cloud_resources=create --extra @/path/to/openstack_task_vars.yml

**NOTE:** Refer to roles/packet_gen/trex/README.md for additional information on cloud_resources.
