To deploy the website we added a file

/home/asmaier/webapps/git/repos/homepage.git/hooks/post-receive

with the content

#!/bin/sh
GIT_WORK_TREE=/home/asmaier/webapps/home git checkout -f master
GIT_WORK_TREE=/home/asmaier/webapps/home git reset --hard

to the git repository on webfaction.

See also:

- https://docs.webfaction.com/software/git.html#pushing-and-pulling-with-a-repository
- http://www.raymonschouwenaar.nl/deploy-website-git-webhosting-webfaction-github-bitbucket/
- https://community.webfaction.com/questions/1246/using-git-with-applications