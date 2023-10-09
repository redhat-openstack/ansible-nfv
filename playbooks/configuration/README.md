# Playbook(s):

* switches_config - The playbook will set provided switches configuration.

* os-net-config-reload - Reload a custom /etc/config.yaml on overcloud nodes.

Reloads a new */etc/os-net-conf/config.yaml* file on overcloud nodes when the
following Jinja2 file is provided:

*{{ os_net_config_reload_path }}/{{ inventory_hostname }}/config.yaml.j2*

The *os_net_config_reload_path* addtional variable must be set.

The playbook read the current */etc/os-net-config.yaml* file from the overcloud
node to instantiate the *config.yam.j2* template which is eventually installed
and reloaded with the *os-net-config* command.

For example, we can change the value of *rx_queue* from 1 to 2 for *dpdkbond0*
from an original *config.yaml* like this:

```
---

network_config:
- type: interface
  name: nic1
  use_dhcp: false
  default: no

- type: interface
  name: nic2
  use_dhcp: false
  addresses:
  - ip_netmask: 192.0.30.23/24
  routes:
  - default: true
    next_hop: 192.0.30.1

- type: linux_bond
  name: bond_api
  use_dhcp: false
  bonding_options: "mode=active-backup"
  dns_servers: ['10.46.0.31', '10.46.0.32']
  members:
    - type: interface
      name: nic3
      primary: true

- type: vlan
  vlan_id: 160
  device: bond_api
  addresses:
  - ip_netmask: 10.10.160.151/24

- type: vlan
  vlan_id: 162
  device: bond_api
  addresses:
  - ip_netmask: 10.10.162.100/24

- type: ovs_user_bridge
  name: br-link0
  mtu: 9000
  use_dhcp: false
  ovs_extra: "set port br-link0 tag=161"
  addresses:
  - ip_netmask: 10.10.161.106/24
  members:
  - type: ovs_dpdk_bond
    name: dpdkbond0
    mtu: 9000
    rx_queue: 1
    members:
      - type: ovs_dpdk_port
        name: dpdk0
        members:
          - type: interface
            name: nic7
      - type: ovs_dpdk_port
        name: dpdk1
        members:
          - type: interface
            name: nic8
```

With the following *config.yaml.j2* template:
```
---

network_config:
- type: interface
  name: nic1
  use_dhcp: false
  default: no

- type: interface
  name: nic2
  use_dhcp: false
  addresses:
  - ip_netmask: {{ network_config[1].addresses[0].ip_netmask }}
  routes:
  - default: true
    next_hop: {{ network_config[1].routes[0].next_hop }}

- type: linux_bond
  name: bond_api
  use_dhcp: false
  bonding_options: "mode=active-backup"
  dns_servers: {{ network_config[2].dns_servers }}
  members:
    - type: interface
      name: nic3
      primary: true

- type: vlan
  vlan_id: {{ network_config[3].vlan_id }}
  device: bond_api
  addresses:
  - ip_netmask: {{ network_config[3].addresses[0].ip_netmask }}

- type: vlan
  vlan_id: {{ network_config[4].vlan_id }}
  device: bond_api
  addresses:
  - ip_netmask: {{ network_config[4].addresses[0].ip_netmask }}

- type: ovs_user_bridge
  name: br-link0
  mtu: 9000
  use_dhcp: false
  ovs_extra: "{{ network_config[5].ovs_extra }}"
  addresses:
  - ip_netmask: {{ network_config[5].addresses[0].ip_netmask }}
  members:
  - type: ovs_dpdk_bond
    name: dpdkbond0
    mtu: 9000
    rx_queue: 2
    members:
      - type: ovs_dpdk_port
        name: dpdk0
        members:
          - type: interface
            name: nic7
      - type: ovs_dpdk_port
        name: dpdk1
        members:
          - type: interface
            name: nic8
```

**Note** - For more details, refer to the role.
