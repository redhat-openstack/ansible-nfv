# Igmp querier

## Description

Configure igmp querier for each network in which it is enabled.
This feature is only valid for ovn. It is configured according to
the following url: https://bugzilla.redhat.com/show_bug.cgi?id=1791815

Used openstack APIs to get the list of ports from which it will be
obtained mac_address and network ids for the ports that will be used
as igmp queriers.

Igmp querier will be configured in the port that conects the network
to the router, so igmp packets will have the gateway ip.

## Role variables
List of networks. For those networks with igmp_querier set to true,
it will be configured igmp querier. Network must have a port connected
to the router. That port will act as igmp querier.
Default value is empty. This parameter is mandatory in order to configure
an igmp querier
```
networks:
  - name: 'data'      
    cloud_name: nfv_tempest      
    gateway_ip: '10.10.124.254'
    igmp_querier: true     
```

Cloud name for the networks
```
cloud_name: nfv_tempest
```
Virtual environment path
```
venv_path: "/tmp/ansible_venv"
```


