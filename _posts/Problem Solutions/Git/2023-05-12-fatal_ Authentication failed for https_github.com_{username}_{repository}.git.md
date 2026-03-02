---
title: 'fatal: Authentication failed for https://github.com/{username}/{repository}.git/'
tags: [problem solution]

category: "Problem Solutions｜Git"
date: 2023-05-12
---

# fatal: Authentication failed for `https://github.com/{username}/{repository}.git/`
## Description
初次使用gitbash push repo時可能會遇到這個問題，有些舊版可能會pop up叫user filled with username/password，但那是非常早期的authentication method，現在需要利用GPG/SSH-Key的方式處理
```bash
$ git push
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/<username>/<repo-name>.git/'
```
<!-- more -->

## Solution-1
1. 產生 SSH Key 並複製 public key
    ```bash
    $ ssh-keygen -t ed25519 -C "youremail@com"
    $ cat ~/.ssh/id_ed25519.pub
    ```
2. 加到 GitHub
    1. 登入 GitHub
    2. Settings → SSH and GPG keys
    3. New SSH Key
    4. 貼上剛剛的 key
3. 改 remote URL
    ```bash
    $ git remote set-url origin git@github.com:<username>/<repo-name>.git
    ```
4. 測試
    ```bash
    $ ssh -T git@github.com
    ...
    Hi <username>! You've successfully authenticated
    ```
5. 如果測試成功就可以正常push了

## Solution-2 (舊版)
According to [this page](https://www.wongwonggoods.com/all-posts/debug_error/git-remote-support/)
Go to [https://github.com/settings/tokens](https://github.com/settings/tokens) (or setting/Developer setting/Tokens (classic)/) and click `Generate new token` to apply a new token.

* If you want to push repo
    Payload: 
    `git remote set-url origin https://ghp_XXXXXXXXXXXXXXXXXXX@github.com/howarder3/test_repo.git`

* If you want to clone your own private repo in new computer
    Payload:
    `git clone https://ghp_XXXXXXXXXXXXXXXXXXX@github.com/howarder3/test_repo.git`