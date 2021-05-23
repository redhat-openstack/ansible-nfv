# Tempest

## Description
Tempest role is dedicated to perform testing execution on TripleO OpenStack environments.

Tempest (not containerized) role will perform the following steps:
  - Install upstream Tempest
  - Install NFV Tempest plugin
  - Install Neutron Tempest plugin
  - Configure Tempest using the python-tempestconf repository
  - Run defined tests

Tempest (containerized) role will perform the following steps:
  - install podman
  - get nfv-container
  - generate tempest configuration
  - run tempest tests
  - saves and parses the results

## Role tags
* run_tempest_test - Executes only the tempest tests.

## Role variables
#### Default variables
containerized rether to use container or plain tempest.
default: false
nfv-tempest-plugin branch to clone.  
Default: master
```
nfv_tempest_branch: 'master'
```
SSH user for the testing image.  
Default user: centos.
```
image_ssh_user: centos
```

Compute microversion to use during tests.  
min_microversion , max_microversion = 2.32  
Refer to [OpenStack Nova API microversion history](https://docs.openstack.org/nova/latest/reference/api-microversion-history.html)
```
compute_min_microversion = 2.32
compute_max_microversion = 2.32
```

Provide required image that will be used for the tempest tests.  
If multiple images are provided, the first one will be used.  
Default image: CentOS-7.
```
images:
  - name: centos7
    url: http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
```

Whether to validate certificates when downloading guest image.
Default image: False.
```
os_image_cert_validation: False
```

Private key and overcloud username for establishing connection between undercloud and overcloud nodes.  
Used for gathering various data like aggregation groups, etc...
```
private_key_dest: /home/stack/.ssh/id_rsa
user_for_overcloud_nodes: heat-admin
```

Flavor name that should be used for tempest tests.  
The flavor that should be created for the tempest test, specified within the openstack_tasks play.  
If not specified, default (first flavor in list) used.
```
#tempest_flavor_name:
```

Path to the tempest config file.  
Variables within the config file will be used by the tempest-nfv-plugin for the tests.  
```
tempest_config: /path/to/the/local/config/file.yml
```

Trigger for generating accounts.yaml file.  
Used in pre-provisioning tempest mode.
```
generate_accounts: false
```

The list of users that accounts.yaml file should be created with.
```
users:
  - name: test_user1
    pass: 12345678
    project: test_project1
    domain: default
    role: member
  - name: test_user2
    pass: 87654321
    project: test_project2
    domain: default
    role: member
```

The path to the accounts.yaml file.  
Used by tempest in pre-provision mode.
```
accounts_file_path: "{{ tempest_dir }}/accounts.yaml"
```

Keep the resources after the tests execution.  
Use "keep_resources: true" to keep the resources.
```
keep_resources
```

Use prepared deployer-input config file for tempest.conf  
A file in the format of tempest.conf that will override the default values.  
The variable has two different options:
* default - Will take the file from the nfv-tempest-plugin repository
* path_to_custom_file - Allows to provide a path to the custom deployer-input file.  
By default the variable is not defined.
```
deployer_input_config
```

If openstack deployed with unsigned service certificate
Use -e validate_certs=false, this will eliminate the check server certificate
error
```
validate__certs
```

Tempest test execution regex.  
The regex can include/exclude required tests for execution.
```
tests_regex: '^tempest_nfv_plugin'
```

Path to the Tempest include file list.  
The list may include regexes on the tests that needs to be executed.
```
tests_include_list: <path_to_the_file_list>
```

#### User defined variables
Append additional tempest.conf variables during it's generation, using the following format:
[GROUP].key=value
```
tempest_extra_vars: ""compute.min_microversion=2,compute.max_microversion=3""
```

nfv-tempest-plugin has the option to enable all provider networks for all interfaces attached to guest interfaces.  
This will set `nfv_plugin_options.test_all_provider_networks` to `true` in tempest.conf.  
This is set to `False` by default.  
For more details refer to [nfv-tempest-plugin patch implementing this feature](https://github.com/redhat-openstack/nfv-tempest-plugin/commit/10b454667a602d08edcfd7ccefc5e9deeab9ebf4):
```ini
enable_test_all_provider_networks: False
```

## Debugging with container tempest
After running the test the tempest container runtime will be removed but image will be saved on the host. to debug just run the container using podman command.
`podman run --network=host --privileged --rm -it --name tempest_nfv --volume /home/stack/tempest:/opt/app-root/src/tempest/container_tempest:Z --volume /home/stack/etc:/opt/app-root/src/tempest/etc:Z -v /etc/pki/:/etc/pki/ -v /etc/hosts:/etc/hosts quay.io/rhos-dfg-nfv/tempest-nfv-plugin:latest /bin/bash`

after running the command you will enter the container there are 2 importent Directoris inside the container: ./etc/ and ./container_tempest which will contain all configuration files etc.

**note!** - make sure paths container name and versions are correct
#### Tests configuration
**Note!** - For the tests configuration, refer to the tempest-nfv-plugin [documentation](https://github.com/redhat-openstack/tempest-nfv-plugin/tree/master/docs).

**Note!** - In case neutron tests should be run, add a regex to include the required tests.
