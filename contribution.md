# Contribution Guidelines

Thank you for choosing to contribute to our project.
Please, follow the instructions below to meet the project contribution guide lines.

- The pull requests for the project accepted via gerrithub review service.
    - Log in to the gerrithub.io(http://gerrithub.io/) using your github account.
    - Once logged in, paste the following url and hit enter:  
      https://review.gerrithub.io/admin/repos/redhat-openstack/ansible-nfv  
      You will be routed to the main page of the project.
    - Choose the preferred method to work with (ssh/http) and clone the repository.
- **Note** - Currently, ansible-nfv project has only linting gate.
  It means that the owner of the patch has the responsibility to test and verify its own patch.
- Once the patch is ready, submit it for the review.
- The linting gate will run and if passed will set the "Verified" label to "+1".  
  In case the linting gate fails, you can check the gate for the errors.  
  There is another way of verify the linting gate.  
  Execute the "./tox_check.sh" script existing in the root of the repository on your local machine.  
  The script will initiate a tox environment and perform the same linting tests, that runs in the gate.  
  The script could be executed before the patch is uploaded as well to indicate the patch owner if there any issue with the linting.
- The owner of the patch, should set his own "Verified" label to "+1" to indicate to the reviewers, that the patch has been verified by the owner.
- The reviewer, by his decision, could verify the patch by him self,  
  but the owner of the patch should not rely on this and appropriately test the patch.
  The main responsibility of the reviewer is to check the structure of the playbook/code and not the functionality.
- Once the patch will get x2 "+2" labels of the "Code-Review", it will be merged by one of the project core maintainers.
- **Note** - Sometimes, the owner of the patch unable to verify the patch functionality due to the specific environment requirements.
  For example, it could be a performance play.
  In such case, the owner of the patch should reach one of the projects core maintainers, and explain the problem.
  We will find a time slot to verify the patch on the required environment.
  Until verified, the patch will be suspended.
  Once verified, it will be reviewed and merged.

For any question or problem, you are welcome to open an issue.

Thank you for your cooperation.
