# iDRAC BIOS Configuration

## Description

The playbook updates the iDRAC BIOS configuration.

This playbook does not require an inventory since it is executed from localhost.

Ansible version >= 2.7 is required for this playbook.

## Inventory
The play requires an inventory file that will describe Dell iDRAC hosts that the playbook should run on.

**Note** - iDRACs are static resources that not changing frequently.

As a result the inventory could be static and not generated dynamically.

The inventory for this playbook should be created by the user.

```ini
[dell_idrac]
dell-idrac1.example.com ansible_host=1.1.1.1
dell-idrac2.example.com ansible_host=1.1.1.2

[dell_idrac:vars]
ansible_user=root
ansible_password=calvin
ansible_connection=local
```

**Note:** `ansible_connection=local` is the recommended way to interact with redfish modules.

If it is required, different credentials and extra variables can be passed via the inventory file. This will allow to run the playbook once and have complete different flows for each host. For more info refer to [Ansible documentation](https://docs.ansible.com/ansible/latest/network/getting_started/first_inventory.html#basic-inventory).

## Variables

Ansible hosts string to use from supplied inventory, for more info refer to [Ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/intro_patterns.html):
```yaml
idrac_inventory_hosts: 'dell-idrac1.example.com,dell-idrac2.example.com'
```

Comma separated list of <BIOS_ATTRIBUTE:BIOS_ATTRIBUTE_VALIUE>, the playbook will split the commas and will iterate on BIOS attributes and their values:
```yaml
idrac_bios_attributes: 'LogicalProc:Enabled'
```

**Note:** This parameter can also be supplied as part of Ansible inventory file.

Power action to perform after applying BIOS configuration.

`PowerGracefulRestart` by default.

Allowed values `'PowerOn', 'PowerForceOff', 'PowerGracefulRestart', 'PowerGracefulShutdown'`.

## Usage

Example on applying a single BIOS attribute on a single host:
```sh
ansible-playbook -i /path/to/inventory playbooks/configuration/dell_idrac_bios_config.yml -e idrac_inventory_hosts='dell-idrac1.example.com' -e idrac_bios_attributes='LogicalProc:Enabled'
```

Example on applying multiple BIOS attributes on a single host:
```sh
ansible-playbook -i /path/to/inventory playbooks/configuration/dell_idrac_bios_config.yml -e idrac_inventory_hosts='dell-idrac1.example.com' -e idrac_bios_attributes='LogicalProc:Enabled,SriovGlobalEnable:Enabled'
```

Example on applying multiple BIOS attribute on multiple hosts:
```sh
ansible-playbook -i /path/to/inventory playbooks/configuration/dell_idrac_bios_config.yml -e idrac_inventory_hosts='dell-idrac1.example.com,dell-idrac2.example.com' -e idrac_bios_attributes='LogicalProc:Enabled,SriovGlobalEnable:Enabled'
```
