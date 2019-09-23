# Openstack instances multiple network configuration

## Description
The script that will be described below, ensures the proper and consistent  
network configuration for the instance with multiple interfaces.

## Issue description
Openstack as the virtualization technology has a known issue with the boot  
of the instance with multiple network interfaces with different IO drivers.  
The problem of the multiple interfaces instance is the fact that the network  
interfaces order do not consistent over the reboot.  
It means that the instance with 2 network interfaces (or more), for for the  
first boot could get the order where NIC "a" will be set as "eth0" and NIC "b"  
will be set as "eth1". But during the next boot, sometimes, the order could  
change and NIC "a" will be allocated as "eth1" and NIC "b" as "eth2".  
**Note** - The above issue happens when the interfaces of the instance are  
using a different libvirt drivers.

Such behavior will cause instance to fail the network start as a mismatch  
between mac address ("/sys/class/net/<interface>/address") of the interface  
and mac address of the "ifcfg" file. As a result, the network service and the  
instance will remain unavailable.

The above behavior will cause default route inside the instance to be  
inconsistent, which could cause SSH connection to be unavailable.  
The switch of the interfaces could even happen on the first boot, and if the  
first interface is a management interface, it will be placed as "eth1".  
As a result, the "default gateway" of the instance will be set incorrectly and  
the instance will be unavailable.

## Solution
To workaround the above known issue, we propose the custom_net_config.py script  
running during cloud-init execution and configure networking, based on neutron  
metadata.


**In details:**  
We are using
[custom_net_script](roles/post_install/openstack_tasks/files/custom_net_config.py)
that relies on the ["cloud-init"](https://cloudinit.readthedocs.io/en/latest/) package.  
The cloud-init package comes with every RHEL and CentOS cloud image by default,  
but could be easily installed on other distributions.  
The cloud-init configures the instance networking by using the metadata passed  
to the instance. For the first boot, the networking is always configured properly  
on the instance interfaces.  
In order to provide consistent configuration dump, the mac address of the  
interface is used as an anchor for the later use and proper allocation of the  
configuration to the proper interface.  
The mac address is taken from the ("/sys/class/net/<interface>/address") and  
compared to the mac address from the "ifcfg" configuration file.  
The script is responsible to keep the the consistent networking configuration  
over any instance reboot state. It does it in the following way:

The script performs the following steps for network dump and restore:
* During the first boot, the interfaces configuration dumped into a json file  
  that stored locally on the instance.
* For each new reboot, the script takes the stored data and restore the configuration  
  of the interfaces.

The "default gateway" issue could be solved by providing the accepted "tag"  
alongside with the NIC that should has the top priority order in the gateways routes.  
The "tag" could be provided via the metadata during the instance creation.  
See Ansible [PR](https://github.com/ansible/ansible/pull/61119) for more details.

The script performs the following steps for the "default gateway":
* The script looks for the "tag" within the instance metadata.  
  A custom "tag" name could be passed by using the "--tag" option.  
  By default - "external".
* If the "tag" found and it match the "tag" name requested by the script:
    * The mac address taken from the NIC with the "tag", resolved in to the  
      interface name and saved into the configuration dump.
    * The second step is to reconfigure the required interface to set the route  
      metric "10" to set the priority for this interface.
    * During the next boot, the route metric restored from the dump config file.

## How to use
The custom_net_script should run on every instance boot.
To ensure this behavior, place the script within the following location on the  
instance - "/var/lib/cloud/scripts/per-boot/custom_net_config.py".

The script does not require any parameters related to the interface configuration.  
If case the "default gateway" should be set on the specific instance port, pass  
the "tag" alonside with the required port. Look on the [PR](https://github.com/ansible/ansible/pull/61119) for the details.  
The default value of the tag is - "external".

In order to provide the script to the instance, during the instance creation,  
use the cloud-config configuration.
The cloud-config has a ["write-files"](https://cloudinit.readthedocs.io/en/latest/topics/examples.html#writing-out-arbitrary-files) module which  
copies the files to the instance.
* Convert the file into the base64 + gzip format hash string.
  ```bash
  $ cat roles/post_install/openstack_tasks/files/custom_net_config.py | gzip | base64
  ```
  The conversion is done in order to minimize the amount of the data that needs  
  to be passed to the instance via the user data.
* Create a cloud-config based format for the write-files module.  
  ```yaml
  #cloud-config
  write_files:
    - path: /var/lib/cloud/scripts/per-boot/custom_net_config.py
      owner: root:root
      permissions: '0755'
      encoding: gzip+base64
      content: |
        H4sIAHVVdV0AA7VaW2/bOBZ+z6/gehDI3nXkzmAfFln4IZumqLFtMkjSDgaZwmAk2tZWFw9JJTWK
        /Pf9ziF1s6UmxXYFJJFE8vBcvnOj8tNfZvdJPlP5g9ju7KbIj34S58V2p5P1xopfXv38D3GtYvFW
        (output omitted)
        (The output hash from the previous command should be placed here)
  ```
* Pass the "cloud-config" data via the user data. See sample config file for example.
