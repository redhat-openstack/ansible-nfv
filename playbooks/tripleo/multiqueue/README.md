# Playbook(s):

* multiqueue_learning: Learn flows received by each queue and pmd cpus for
  specific rates

The goal of this playbook is to learn about multiqueues:
* Sending several flows, knowing which flow will arrive to each queue so that
  we will be able to inject traffic to specific queues
* Injecting at specific rates, knowing which cpu will the pmd use.
  Interpolating these values it would be able to estimate cpu usage.

The flow of this playbook is the following one:
1. pin physical queues to different PMDs. The goal is not to have 2 physical
   queues of the same port in the same pmd as this will cause that a single
   virtual queue will be used for the traffic of those physical queues.
2. Configure dpdk and run testpmd in testpmd vm enabling logs
3. From trex vm, execute multiqueue.py script to generate several packets.
   Those packets will arrive to testpmd that will generate testpmd.log with
   information about the packets received and the queues that received each
   packet.
4. Copy testpmd.log to trex vm and execute multiqueue.py to parse it and
   generates queues.json. This file will have a list of ips for each queue.
5. Stop testpmd and run again without logs
6. Configure dpdk, huge pages, trex and run trex in trex vm
7. Inject from trex in 2 queues placed in different pmd cores at different
   rates. Get the cpu rate of those pmds.
8. Add those values to the queues.json file
9. Remove the cpu pinning done in step 1

testpmd and trex vms together with queues.json file are ready to execute
multiqueue/autobalance regression from tempest

queues.json filed generated  has the following format:
[                             --> for each port in trex vm
    {
        "name": "eth1",       --> kernel name for this port
        "queues": {           --> list of queues
            "1": {            --> queue id, as returned by ovs command
                "pps": 0.5,   --> pps (mpps) used to send to this queue
                "rate":  0.8, --> pps used for learning pmd usage
                "isg": 0,     --> delay in us for this stream
                "ips": [      --> list of ips that will be used
                    "48.0.0.1",
                    "48.0.0.3",
                    "48.0.0.4",
                ],
                "hyp_queues": [ --> queueus in hypervisor
                    {
                        "port": "dpdk2", --> port name
                        "queue_id": 0,   --> queue id
                        "pmd_usage": 16  --> pmd usage when injecting rate
                    },
                    {
                        "port": "vhu0f898af0-58",
                        "queue_id": 1,
                        "pmd_usage": 15
                    }
                ]
            },
            "2": {
                "pps": 0.1,
                "isg": 0,
                "ips": [
                    "48.0.0.2",
                    "48.0.0.7",
                    "48.0.0.8",
                ],
                "hyp_queues": [
                    {
                        "port": "dpdk2",
                        "queue_id": 1,
                        "pmd_usage": 5
                    },
                    {
                        "port": "vhu0f898af0-58",
                        "queue_id": 2,
                        "pmd_usage": 4
                    }
                ]
            },


# Variables:

trex vm cores

```
trex_lcores: '2-11'
```

testpmd cpu pinning

```
testpmd_lcores: '1-7'
```

testpmd forwarding cores

```
testpmd_forward_cores: 6
```

testpmd rx queues

```
testpmd_rxq: 3
```

testpmd tx queues

```
testpmd_txq: 3
```

testpmd path (for rhel 8.4 vm)

```
testpmd_bin: "/root/dpdk/build/app/dpdk-testpmd"
```

affinity used for learning mode

```
pmd_rxq_affinity: [ {'interface': 'dpdk2', 'pmd_rxq_affinity': '0:3,1:5,2:7'},
                    {'interface': 'dpdk3', 'pmd_rxq_affinity': '0:3,1:5,2:7'} ]
```

set down interfaces in OVS bridge

```
testpmd_down_interfaces: [{'bridge': '<BRIDGE>', 'interface': '<IFACE>'}]
```

multiqueue config

```
multiqueue_config: True
```

testpmd_log

```
testpmd_log: /tmp/testpmd.log
```

rates used for learning hypervisor ports (mpps)

```
port0_rate: 0.8
port1_rate: 0.4
```

injection time in seconds
```
duration: 40
```

file with the queues learned
```
queues_json: "/tmp/queues.json"
```
