# Guest Image Customization For Perfomance Usecases

## Description
The prepare_performance_images role performs the following tasks:
- Prepares repos for RHEL/CentOS 7 images
- Clones Trex from upstream repo to guest image
- Clones DPDK from upstream repo and compiles it

**Note!** - virt_customize moduless are planned to be shipped in this repo until they're available in PyPI
**Note!** - Inventory file is required if attempting to run on default undercloud node
**Note!** - DPDK is being compiled without:
* [rt-kni](https://doc.dpdk.org/guides/prog_guide/kernel_nic_interface.html) - This feature allows DPDK to leverage it's user space capabilites for NICs bound to kernel, disabling it due to:
    * Requiring kernel modules during compilation, which will require additional logic for virt-customize
    * Not relevent to NFV-QE usecases
* [UIO](https://doc.dpdk.org/guides/linux_gsg/linux_drivers.html#uio) - Basic kernel module which configures the device, maps device mermory to user space and handles interrupts, disabling it due to:
    * Requiring kernel modules during compilation, which will require additional logic for virt-customize
    * Not relevent to NFV-QE usecases, we use vfio instead

* Repos
    * Uses CentOS public repos to customize RHEL/CentOS images
* Prepare Trex
    * Clones Trex binaries from repo
* Prepare DPDK
    * Clones DPDK binaries from repo
    * Compiles DPDK binaries

## Run triggers
* prepare_repo - Executed if 'true'. True by default.
* prepare_trex - Executed if 'true'. True by default.
* prepare_dpdk - Executed if 'true'. True by default.

## Role variables
#### Image details
**Note:** If running on local host, consider using `--connection=local` (refer to [Ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_delegation.html#local-playbooks))
Ansible host to run customization on (Tested on Fedora/RHEL/CentOS), by default undercloud node:
```
customization_host: ''
```

URL of guest image to be downloaded
```
guest_image: 'https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2'
```

Output directory/file of fetched image:
```
guest_image_output: '/tmp/'
```

Enable debug output of virt-customize action:
```
guest_debug: False
```

#### Customization variables
DPDK version to be cloned
```
dpdk_branch: v17.05
```

Trex version to be cloned
```
trex_branch: v2.43
```

### Repo variables
Temporary directory to store repo file on host:
```
repo_dir: '/tmp/guest_repos'
```

List of repos to be created and uploaded to guest image, uses the following arguments from Ansible [yum_repository](https://docs.ansible.com/ansible/latest/modules/yum_repository_module.html) module: `name`, `description`, `state`, `mirrorlist`, `gpgcheck`, `gpgkey` and `file`.
```
guest_repos:
  - name: 'base' # Mandatory
    description: 'CentOS-$releasever - Base' # Not mandatory, will be generated based on name
    state: 'present' # Mandatory
    mirrorlist: 'http://mirrorlist.centos.org/?release=7&arch=$basearch&repo=os' # Not mandatory
    baseurl: 'http://mirror.centos.org/centos/7/os/$basearch/' # Mandatory
    gpgcheck: True # Not mandatory
    gpgkey: 'https://www.centos.org/keys/RPM-GPG-KEY-CentOS-7' # Not mandatory
    file: "/tmp/guest_repos/centos" # Not mandatory, will be generated based on repo_dir and name
```

### DPDK Variables

Directory on guest image to clone DPDK repo to:
```
dpdk_dir: '/root/dpdk'
```

Log file for DPDK flow
```
dpdk_customization_log: '/root/dpdk/customization.log'
```

DPDK git URI:
```
dpdk_git: 'git://dpdk.org/dpdk'
```

### Trex Variables

Trex binaries URL:
```
trex_url: 'http://trex-tgn.cisco.com/trex/release'
```

Directory on guest to contain DPDK binaries in:
```
trex_dir: '/opt/trex/'
```

### Trafficen Variables
Trafficgen git URI:
```
trafficgen_git: 'https://github.com/atheurer/trafficgen'
```

Directory on guest to contain trafficgen scripts in:
```
trafficgen_dir: '/opt/trafficgen'
```

Trafficgen scripts version to clone:
```
trafficgen_branch: master
```

### User customization Variables
Dictoniary containg users to be created:
```
custom_users:
  - user: root
    password: 12345678
```

### User defined Variables

A list of additional user supplied commands to run (None by default):
```
user_commands: 
  - cat /etc/resolv.conf
  - echo '1' > /dev/null
```

A list of additional user supplied packages to be installed (None by default):
```
user_packages:
  - mlocate
  - vim
```

## Examples
The examples of running the playbook:

Retrieve CentOS image, prepare CentOS repo, install default DPDK and Trex binaries:
```
ansible-playbook playbooks/images/prepare_performance_images.yml
```

Specify custom repo file for image
```
ansible-playbook playbooks/images/prepare_performance_images.yml -e @/path/to/repo_vars.yaml
```

Don't prepare repos for guest image
```
ansible-playbook playbooks/images/prepare_performance_images.yml -e prepare_repo=False
```

Specify different RHEL/CentOS/Fedora image to be customized:
```
ansible-playbook playbooks/images/prepare_performance_images.yml -e guest_image="http://url-to-image.com"
```

Opt out of DPDK/Trex customization:
```
ansible-playbook playbooks/images/prepare_performance_images.yml -e prepare_dpdk/trex=False
```
