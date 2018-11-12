plugin_type: other
subparsers:
    tripleo-inventory:
        description: Create inventory file from an existing tripleo envrionemt.
        include_groups: ['Ansible options', 'Inventory', 'Common options', 'Answers file']
        options:
          host:
              type: Value
              help: Undercloud/Hypervisor host name/ip
              required: yes
          ssh-key:
              type: Value
              help: SSH key to be used for host
              default: ''
          ssh-pass:
              type: Value
              help: |
                  SSH password for host.
                  When this option is used dynamic ssh key will be generated and used.
              default: ''
          user:
              type: Value
              help: Undercloud user. Default - stack
              default: root
          setup-type:
              type: Value
              help: |
                  Define the type of the environment.
                  For baremetal environment use - baremetal
                  and for virt or hybrid environment use - virt
              choices:
                  - baremetal
                  - virt
              default: virt
          overcloud-user:
              type: Value
              help: Overcloud user
              default: heat-admin
          venv-path:
              type: Value
              help: Virtual environment path
              default: /tmp/ansible_venv
          undercloud-groups:
              type: Value
              help: |
                  Define the groups, Undercloud host should be added to.
                  multiple groups should be separated by the comma.
              default: undercloud,tester
          hypervisor-groups:
              type: Value
              help: |
                  Define the groups, hypervisor host should be added to.
                  multiple groups should be separated by the comma.
              default: hypervisor
          undercloud-only:
              type: Bool
              help: |
                  Create inventory file with the underlcoud details only if required.
                  By default the variable is used as false.
                  Could be executed as an extra vars - true
              default: no