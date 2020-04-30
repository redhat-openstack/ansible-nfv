Moleculte Test Execution
========================

Executing molecule tests in local environment
---------------------------------------------
Depending on the role's usecase, either docker container or vagrant vm
will be used for tests. For cases where a grub changes are requird like tuned
configs, vagrant vms are used.

```
git clone https://github.com/redhat-openstack/ansible-nfv.git
cd ansible-nfv
./tools/configure-env.sh
source .venv/bin/activate

cd roles/tuning/tuned_configuration
molecule test
```

Enable python3 on RHEL 7.x
--------------------------
```
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-$(rpm -E '%{rhel}').noarch.rpm
```
