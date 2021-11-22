# Playbook(s):

* trex/prepare_resources - Prepare/Create resources  
  Roles that are used in the playbook:  
  * post_install/openstack_tasks
  * post_install/dynamic_host_inventory

* trex/performance_scenario - Execute performance scenario using trex server.  
  Roles that are used in the playbook:  
  * post_install/openstack_tasks
  * post_install/dynamic_host_inventory
  * packet_gen/trex/compute_tuning
  * packet_gen/trex/launch_fio
  * packet_gen/trex/trex_instance_config
  * packet_gen/trex/bind_dpdk_nics
  * packet_gen/trex/launch_testpmd
  * packet_gen/trex/launch_trex
  * packet_gen/trex/binary_search

* iperf/performance_scenario - Execute performance scenario using iperf.
  Roles that are used in the playbook:
  * packet_gen/iperf/server
  * packet_gen/iperf/client
  
* trex/multiqueue_learning - Learns which queue receives it flow and creates
  a file in trex vm with that information
  Roles that are used in the playbook:
  * post_install/openstack_tasks
  * post_install/dynamic_host_inventory
  * packet_gen/trex/trex_instance_config
  * packet_gen/trex/bind_dpdk_nics
  * packet_gen/trex/launch_testpmd
  * packet_gen/trex/multiqueue_learning
  * tuning/cpu_pinning_huge_pages
  * packet_gen/trex/launch_trex

**Note** - For more details, refer to the role.
