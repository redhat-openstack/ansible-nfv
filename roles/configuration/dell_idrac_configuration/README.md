# iDRAC BIOS Configuration

## Description

The playbook updates the iDRAC BIOS configuration.

This playbook does not require an inventory since it is executed from localhost.

Ansible version >= 2.7 is required fro this playbook.

## Variables

Comma separated list of iDRAC URIs (excluding HTTP/HTTPS), the playbook will split the comma and will iterate on hosts:
```yaml
idrac_hosts: 'dell-idrac1.example.com,dell-idrac2.example.com'
```

Comma separated list of <BIOS_ATTRIBUTE:BIOS_ATTRIBUTE_VALIUE>, the playbook will split the commas and will iterate on BIOS attributes and their values:
```yaml
idrac_bios_attributes: 'LogicalProc:Enabled'
```

iDRAC username to use in authentication:
```yaml
idrac_user: 'root'
```

iDRAC password to use in authentication:
```yaml
idrac_password: 'password'
```

Power action to perform after applying BIOS configuration.

`PowerGracefulRestart` by default.

Allowed values `'PowerOn', 'PowerForceOff', 'PowerGracefulRestart', 'PowerGracefulShutdown'`.

## Usage

Example on applying a single BIOS attribute on a single host:
```sh
ansible-playbook playbooks/configuration/dell_idrac_bios_config.yml -e idrac_hosts='dell-idrac1.example.com' -e idrac_bios_attributes='LogicalProc:Enabled' -e idrac_user='root' -e idrac_password='password'
```

Example on applying multiple BIOS attributes on a single host:
```sh
ansible-playbook playbooks/configuration/dell_idrac_bios_config.yml -e idrac_hosts='dell-idrac1.example.com' -e idrac_bios_attributes='LogicalProc:Enabled,SriovGlobalEnable:Enabled' -e idrac_user='root' -e idrac_password='password'
```

Example on applying multiple BIOS attribute on multiple hosts:
```sh
ansible-playbook playbooks/configuration/dell_idrac_bios_config.yml -e idrac_hosts='dell-idrac1.example.com,dell-idrac2.example.com' -e idrac_bios_attributes='LogicalProc:Enabled,SriovGlobalEnable:Enabled' -e idrac_user='root' -e idrac_password='password'
```
