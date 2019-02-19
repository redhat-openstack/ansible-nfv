# Trex

## Description
Generates traffic on Trex instance to DuT instance using 'trafficgen' repo

## Role Variables
### Trex Instance Variables
Trex guest instance name or UUID to be used in API queries
```
trex_server: 'trex'
```

Trex public mangement IP address which can be used to access the instance, will be attempted to be discovered via APIs if not specified
```
trex_server_mgmt_ip: "10.11.12.13"
```

Trex user credentials used to login into an instance, can be accessed via username+password or username+ssh_key
```
trex_server_user: 'root' # Username used to log in
trex_server_password: '12345678' # Password used to log in
trex_ssh_key: '/path/to/keys' # SSH key used to log in
trex_ssh_pass: 'ssh_secret' # SSH Secret
```

Whether to luanch Trex server
```
trex_launch: True
```

### Trex Binaries Variables
Trex CLI to run, overrides default and other variables
```
trex_cmd: /opt/trex/current/t-rex-64 -i -c 8 --cfg /etc/trex_cfg.yaml"
```

Number of cores to be assigned to Trex process:
```
trex_process_cores: 8
```

Additional CLI arguments to pass to default trex commnad:
```
trex_process_extra_args: '-a -m 1 -f stl/imix_1pkt.yaml'
```

### TestPMD Binaries Variables
TestPMD CLI to run, overrides default and other variables:
```
testpmd_cmd: "/root/dpdk/build/app/testpmd -l 10,11 -n 4 --socket-mem 1024 -- --nb-cores=2 --auto-start --rxd=1024 --txd=1024"
```

TestPMD lcores:
```
testpmd_lcores: '7,10,11'
```

Test PMD memory channels
```
testpmd_mem_channels: 4
```

TestPMD socket meomry:
```
testpmd_socket_mem: 1024
```

TestPMD forward cores:
```
test_pmd_forward_cores: 2
```

Test PMD RX queue:
```
testpmd_rxd: 1024
```

Test PMD TX queue:
```
testpmd_txd: 1024
```
### binary-search script Variables
Binary search to run, overrides default and other variables
```
binary_search_cmd: "/opt/trafficgen/binary-search.py --traffic-generator trex-txrx --frame-size 64 --max-loss-pct 0.00 --send-teaching-warmup  --dst-macs 52:54:00:00:00:00,52:54:00:00:00:01 --num-flows 1"
```

Trex frame size to be generated:
```
trex_frame_size: 64
```

Trex max % of lost packets acceptable
```
trex_max_lost_pct: 0.00
```

DuT(Device under test) destination MAC addresses:
```
dut_macs: '52:54:00:00:00:00,52:54:00:00:00:01'
```

Number of flows to use when generating traffic:
```
trex_flows: 1
```

Rate per device:
```
trex_rate: 2
```

## Example
Examples of running this playbook:

Run performance on DuT of type SR-IOV:
```
ansible-playbook playbooks/packet_gen/trex/generate_traffic.yml -e trex_server=trex -e dut_server=testpmd_sriov_vf_dut -e dut_type=sriov
```

Run performance on DuT of type DPDK:
```
ansible-playbook playbooks/packet_gen/trex/generate_traffic.yml -e trex_server=trex -e dut_server=testpmd_dpdk_dut -e dut_type=dpdk
```
