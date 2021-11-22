# Multiqueue/autobalance injection

## Description
Role used to inject to a specific number of queues or to learn about different queues

It will execute multiqueue.py script which has the following options:
usage: multiqueue.py [-h] --action {learning,parse,gen_traffic}
                     [--packets [PACKETS [PACKETS ...]]]
                     [--traffic_json TRAFFIC_JSON] [--log LOG]
                     [--duration DURATION] [--multiplier MULTIPLIER]
                     [--pps PPS]

It has 3 main functions:
* learning: Using scapy it generates several packets with different source or destination ip
  address. Each packet will have different size too so that it can be recognized either by the ip
  or the packet size. In testpmd it is possible to log each packet received in each queue, but it
  is not printed out the ip, so using a map between ip and packet size it is possible to know
  which ip is being received in that queue
* parse: parse testpmd log. It gets which queue received each packet
* gen_traffic: generate traffic using trex, it is possible to send traffic to specific queues

Examples on how to use it:
* learning:
  multiqueue.py --packets 0 40
  It will generate packets from 48.0.0.1 to 48.0.0.40. It will generate traffic in both interfaces,
  in one interface this will be source ip while in te other it will be destination ip
  
* parse:
  multiqueue.py --packets 0 40 --log /tmp/testpmd.log --traffic_json /tmp/queues.json
  It will parse testpmd log and generate queues.json file with a list of ip address received by
  each port and queue.
  
* gen_traffic:
  multiqueue.py --traffic_json /tmp/queues.json --duration 60 --multiplier 1 \
                --pps "[{"0": 0.5},{"1": 0.8}]"
  Using trex it will inject traffic to the specific queues. In this case, it will inject 0.5 mpps
  to port 0 queue 0 and 0.8 mpps to port 1 queue 1. Ports, queues and flows to used are defined in
  queues.json file. Injection duration will be 60 seconds. With multiplier parameter it can inject
  at higher rates, for example, if multiplier would have been 10, injections would be at 5 and 8
  mpps.
  
## Variables

Multiqueue packet generator absolute path

```
mq_bin: "{{ trafficgen_dir }}/{{ mq_file }}"
```

Packet generator will start using ips from base_ip + min_packet_index

```
min_packet_index: 0
```

Packet generator will start using ips until base_ip + min_packet_index + max_packet_index

```
max_packet_index: 40
```

testpmd log file

```
testpmd_log: "/tmp/testpmd.log"
```

File generated with the mapping of queues and ips

```
queues_json: "/tmp/queues.json"
```

Mode used in multiqueue traffic generator: available: parse, learning, gen_traffic

```
action: "learning"
```

Duration of injection when using gen_traffic mode

```
duration: 180
```

Increase traffic rate when using gen_traffic mode

```
multiplier: 1
```

Activate nics, for learning mode in which dpdk is not used

```
activate_nics: True
```

Rates for each queue

```
pps: []
```