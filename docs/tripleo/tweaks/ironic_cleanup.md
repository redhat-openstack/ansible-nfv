# Ironic cleanup

## Description

Performs ironic cleanup steps on baremetal nodes.

This playbook requires Ansible inventory of your deployment.  
Generate an inventory using [tripleo-inventory playbook](../post_install/tripleo_inventory.md).

## Playbook Variables

### Cloud

Path to file containing undercloud credentials that will be sourced.

`/home/stack/stackrc'` by default.

```yaml
undercloud_credentials_file: '/home/stack/stackrc'
```

### Cleanup

Cleanup steps to be performed by ironic.  
Steps must be in JSON/YAML format.

`[{"interface": "deploy", "step": "erase_devices_metadata"}]'` by default.

```yaml
cleanup_steps:
  - interface: "deploy"
    step: "erase_devices_metadata"
```

Amount of retries to be performed by Ansible when querying node status during cleanup.

`60` by default.

```yaml
cleanup_retries: 60
```

Seconds to wait before retries.

`5` by default.

```yaml
cleanup_delay: 5
```

## Example

Perform device metadata cleanup (default scenario):

```bash
ansible-playbook playbooks/tripleo/tweaks/ironic_cleanup.yaml
```
