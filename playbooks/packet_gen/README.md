# Playbook(s):

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

* trex/performance_scenario_with_iperf_hypervisor_stress - Execute performance scenario using trex while stressing hypervisor nodes with iperf.  
  This playbook is suitable for deployments with QoS(Quality of Service) applied to OpenStack control plane.  
  The following parameters are required to be supplied by user::
    * iperf_hypervisor_interface - Hypervisor interface that will bound to iperf server
    * iperf_server_hypervisor - Hypervisor name that will host iperf server, this name must be defined in Ansible inventory
    * iperf_client_hypervisor - Hypervisor name that will host iperf client, this name must be defined in Ansible inventory
    * hypervisor_group - Hypervisor group name, this name must be defined in Ansible inventory
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

**Note** - For more details, refer to the role.
