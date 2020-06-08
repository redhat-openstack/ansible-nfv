# Playbook(s):

* trex/performance_scenario - Execute performance scenario using trex server.  
  Roles that are used in the playbook:  
  * post_install/dynamic_instances_count
  * post_install/prepare_dynamic_instances
  * post_install/openstack_tasks
  * post_install/dynamic_host_inventory
  * packet_gen/trex/compute_tuning
  * packet_gen/trex/launch_fio
  * packet_gen/trex/trex_instance_config
  * packet_gen/trex/bind_dpdk_nics
  * packet_gen/trex/launch_testpmd
  * packet_gen/trex/launch_trex
  * packet_gen/trex/binary_search
* moongen/moongen-install - Installs moongen server (deprecated).
* moongen/moongen-run - Execute performance scenario using moongen server (deprecated).

**Note** - For more details, refer to the role.
