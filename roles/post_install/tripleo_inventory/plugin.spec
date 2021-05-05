################################################
# The file is being used by infrared as plugin #
################################################

plugin_type: other
subparsers:
    tripleo-inventory:
        description: Generate an inventory from the existing tripleo environment.
        include_groups: ["Ansible options", "Inventory", "Common options", "Answers file"]
        groups:
            - title: Host variables
              options:
                  host:
                      type: Value
                      help: Hypervisor/Undercloud host name/ip
                      required: yes
                  user:
                      type: Value
                      help: SSH user to be used for the host connection
                      default: root
                  ssh-key:
                      type: Value
                      help: SSH key to be used for the host connection
                      default: ''
                  ssh-pass:
                      type: Value
                      help: |
                          SSH password to be used for the host connection.
                          When this option is used, dynamic ssh key will be generated and used.
                      default: ''

            - title: Environment variables
              options:
                  setup-type:
                      type: Value
                      help: |
                          Define the type of the environment.
                          Possible values - virt, baremetal.
                          For virt or hybrid, use - virt.
                          For baremetal, use - baremetal
                      choices:
                          - 'virt'
                          - 'baremetal'
                      default: 'virt'
                  overcloud-user:
                      type: Value
                      help: User used for connection to overcloud nodes
                      default: 'heat-admin'
                  custom-undercloud-user:
                      type: Value
                      help: Define custom undercloud user of required
                      default: 'stack'
                  undercloud-groups:
                      type: Value
                      help: |
                          Define the groups, Undercloud host should be added to.
                          Multiple groups should be separated with comma.
                      default: 'undercloud,tester'
                  hypervisor-groups:
                      type: Value
                      help: |
                          Define the groups, Hypervisor host should be added to.
                          Multiple groups should be separated with comma.
                      default: 'hypervisor,shade'
                  undercloud-only:
                      type: Bool
                      help: |
                          Create inventory file with the underlcoud details only.
                          Could be used when overcloud nodes are unreachable.
                      default: 'false'
                  venv-path:
                      type: Value
                      help: Virtual environment path
                      default: '/var/tmp/venv_shade'
