# Playbook(s):

* tempest - Install, configure and execute nfv based tests in tempest.  
  Roles that are used in the playbook:  
  * post_install/openstack_tasks
  * tester/tempest
* tempest_with_external_resources - Install, configure and execute nfv based tests  
  in tempest with creation of the resources by the `openstack_tasks` role.  
  Roles that are used in the playbook:  
  * post_install/openstack_tasks
  * tester/tempest
* crossnuma-performance - Deprecated performance playbook. Will be removed.
* testpmd-deploy-run - Deprecated performance playbook. Will be removed.

**Note** - For more details, refer to the role.
