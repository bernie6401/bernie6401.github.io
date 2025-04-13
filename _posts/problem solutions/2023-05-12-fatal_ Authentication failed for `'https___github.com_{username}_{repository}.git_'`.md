---
title: 'fatal: Authentication failed for `''https://github.com/{username}/{repository}.git/''`'
tags: [problem solution]

category: "Problem Solutions"
---

# fatal: Authentication failed for `'https://github.com/{username}/{repository}.git/'`
<!-- more -->
###### tags: `problem solution`

## Solution
According to [this page](https://www.wongwonggoods.com/all-posts/debug_error/git-remote-support/)
Go to [https://github.com/settings/tokens](https://github.com/settings/tokens) (or setting/Developer setting/Tokens (classic)/) and click `Generate new token` to apply a new token.

* If you want to push repo
Payload: 
`git remote set-url origin https://ghp_XXXXXXXXXXXXXXXXXXX@github.com/howarder3/test_repo.git`

* If you want to clone your own private repo in new computer
Payload:
`git clone https://ghp_XXXXXXXXXXXXXXXXXXX@github.com/howarder3/test_repo.git`