#!/bin/bash
# Execute molecule testing for each role that contains molecule scenario

set -eo pipefail

if [[ ! -n "${TEST_HOST}" && ! -n "${TEST_SSH_KEY}" ]]; then
    echo "Some of the scenarious require the following env variables:"
    echo -e "TEST_HOST\nTEST_SSH_KEY\n"
    echo "Set the env variables and rerun the test."
    echo "For explanation of the env variables, look for the openstack_task molecule role."
    exit 1
fi

runs=0
failed_runs=0
declare -a tested_roles
declare -a failed_roles

logs_dir=$(pwd)/molecule_logs
rm -rf $logs_dir
mkdir $logs_dir

# Many of the ansible-nfv roles tests require access to the working Openstack environment.
# As the gate that is used is fully virtual and not accessible from outside, we are
# using tripleo_inventory role to provide that access.
# In order to minimize the time of tests execution and not to rerun the tripleo_inventory
# generation for each role, it will be done once when molecule_test.sh script executed.
# When a role tested separately, it will generate the inventory by itself.
echo "Generating the inventory for the roles."
export MOLECULE_INVENTORY_PATH=$(pwd)/inventory
ansible-playbook playbooks/tripleo/post_install/tripleo_inventory.yml \
-e host="${TEST_HOST}" -e ssh_key="${TEST_SSH_KEY}" -e setup_type=virt
export TEST_INV_GENERATED=true
export ANSIBLE_COLLECTIONS_PATH=/tmp/.collectinos

echo installing requirements
ansible-galaxy collection install -r requirements.yaml -p $ANSIBLE_COLLECTIONS_PATH

molecules="$(find roles/ -name molecule -type d)"
for molecule in $molecules; do
    pushd $(dirname $molecule)
    export ANSIBLE_LOG_PATH=$logs_dir/$(basename $(dirname $molecule)).log

    if ! molecule test; then
        failed_runs=$((failed_runs + 1))
        failed_roles+=($(dirname $molecule))
    fi
    runs=$((runs + 1))
    tested_roles+=($(dirname $molecule))
    popd
done

echo -e "\n################"
echo "Tests results:"
if [[ $failed_runs -ne 0 ]]; then
    echo -e "\nFailed $failed_runs/$runs molecule tests"
    echo -e "\nTested roles:"
    for role in "${tested_roles[@]}"; do
        echo "- $role"
    done
    echo -e "\nFailed molecule roles:"
    for role in "${failed_roles[@]}"; do
        echo "- $role"
    done
    exit 1
fi

echo -e "\nRan sucesfully $runs molecule tests"
echo -e "\nTested roles:"
for role in "${tested_roles[@]}"; do
    echo "- $role"
done
echo removing requirements installed for test
rm -rf $ANSIBLE_COLLECTIONS_PATH
echo -e "################\n"
