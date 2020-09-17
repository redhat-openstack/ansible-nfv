# Guest Image Customization For Perfomance Usecases

## Description
The prepare_performance_images role performs the following tasks:
- Prepares repos for RHEL/CentOS 7 images
- Clones Trex from upstream repo to guest image
- Clones DPDK from upstream repo and compiles it
- Clones fio from upstream repo and compiles it
- Performs custom user operations

**Note!** - Inventory file is required if attempting to run on default undercloud node

**Note!** - This playbook was designed and supporting customization of CentOS 7.6/RHEL 7.6, other images are not tested

**Note!** - Mellanox drivers are aligned according to Trex's recommendation.

* Repos
    * Uses CentOS public repos to customize RHEL/CentOS images
* Prepare Trex
    * Clones Trex binaries from repo
* Prepare DPDK
    * Clones DPDK binaries from repo
    * Compiles DPDK binaries
* Prepare fio
    * Clones fio binaries from repo
    * Compiles fio binaries
* User operations
    * Install custom packages
    * Populate users
    * Perform commands

## Run triggers
* prepare_repo - Executed if 'True'. `True` by default.
* prepare_trex - Executed if 'True'. `True` by default.
* prepare_dpdk - Executed if 'True'. `True` by default.
* prepare_fio - Executed if `True`. `True`  by default.

## Role variables
#### Image details
**Note:** If running on local host, consider using `--connection=local` (refer to [Ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_delegation.html#local-playbooks))
Ansible host to run customization on (Tested on Fedora/RHEL/CentOS), by default undercloud node:
```
customization_host: ''
```

URL of guest image to be downloaded
```
guest_image: 'https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1811.qcow2'
```

Output directory/file of fetched image:
```
guest_image_output: '/tmp/'
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

DPDK version to be cloned
```
dpdk_branch: v20.05
```

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

Trex version to be cloned
```
trex_branch: v2.82
```

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

### fio variables

fio git URI:
```
fio_git: 'git://git.kernel.dk/fio.git'
```

Directory on guest to contain fio binaries:
```
fio_dir: '/root/fio'
```

fio branch to be cloned:
```
fio_branch: 'fio-3.20'
```

Log file for fio:
```
fio_customization_log: "{{ fio_dir }}/customization.log"
```

### Mellanox variables

Compile Mellanox drivers in the guest:
```
compile_mlx_driver: False
```

Mellanox OFED drivers URL:
```
mellanox_drivers_url: 'http://content.mellanox.com/ofed/MLNX_OFED-4.6-1.0.1.1/MLNX_OFED_LINUX-4.6-1.0.1.1-rhel7.6-x86_64.iso'
```

Mellanox drivers directory location to be downloaded:
```
mellanox_drivers: "/tmp/{{ mellanox_drivers_url | basename }}"
```

Mellanox OFED CLI installation arguments:
```
mlex_ofed_install_args: "--force --without-fw-update --with-mft --with-mstflint --dpdk --upstream-libs -k {{ image_default_kernel }}"
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

Generate image with compiled mlx driver:
```
ansible-playbook playbooks/images/prepare_performance_images.yml -e compile_mlx_driver=True
```
