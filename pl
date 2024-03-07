ansible-playbook -v                         -i inventory                         playbooks/packet_gen/trex/performance_scenario.yml                         -e @/tmp/dpdk/perf_resources_config.yml -e binary_perf_log=/tmp/dpdk_performance.log                         -e dut_group=dpdk_dut -e dut_type=dpdk -e testpmd_lcores=3,4,5 -e trex_rate=2 -e emc_insert_inv_prob=100                         -e clone_traffic_gen_repo=false -e @/tmp/dpdk/perf_instances.yml                         -e private_key_fetch_location=/home/ciuser/test_keypair.key -vv




