# Contribution Guidelines

Thank you for choosing to contribute to our project.
Please, follow the instructions below to meet the project contribution guide lines.

- The pull requests for the project accepted via gerrithub review service.
  Use the following steps to prepare the environment:
    - Clone the repository to your local env and enter the directory:
        $ git clone git@github.com:redhat-openstack/ansible-nfv.git
        $ cd ansible-nfv/
    - Create a virtualenv, activate and install the requirements and test-requirements:
        $ virtualenv /tmp/ansible_nfv_venv
        $ source /tmp/ansible_nfv_venv/bin/activate
        $ pip install -r requirements.txt -r test-requirements.txt
    - Add gerrithub remote to your repo:
      **Note** - Make sure to set your GitHub username in the command below:
        $ git remote add gerrit ssh://<your_ssh_username>@review.gerrithub.io:29418/redhat-openstack/ansible-nfv.git
    - Create the patch branch from the "devel" branch:
        $ git checkout -b patch_branch devel
    - Create the required changes, add and commit the changes.
    - Submit the patch.
      **Tip** - Use the "git review" (somethimes needs to be installed separatelly) command instead of "git push".
      It will ease the work with the gerrit system.
- **Note** - Currently, ansible-nfv project has only linting gate.
  It means that the owner of the patch has the responsibility to test and verify its own patch.
- Once the patch is ready, submit it for the review.  
- The linting gate will run and if passed will set the "Verified" label to "+1".  
  In case the linting gate fails, you can check the gate for the errors.  
  There is another way of verify the linting gate.  
  Execute the "./tox_check.sh" script existing in the root of the repository on your local machine.  
  The script will initiate a tox environment and perform the same linting tests, that runs in the gate.  
  The script could be executed before the patch is uploaded as well, indicates patch owner in case of linting errors/warnings.
- Patch owner, should set Verified "+1" label to indicate patch has been verified/tested by him
- The reviewer, could choose verifying the patch.  
  Patch owner should not rely on the above, and test/verify the changes.  
  Reviewer responsibility concerns code structure, logic and not testing it.
- Once the patch will get x2 "+2" labels of the "Code-Review", it will be merged by core maintainers.
- **Note** - In cases, patch owner could not test/verify its changes, due to the specific environment requirements,
  his responsibility to reach our core reviewers and explain the needs.  
  Core reviewers will find the the resource and time to verify the patch.

For any question or problem, you are welcome to open an issue.

Thank you for your cooperation.
