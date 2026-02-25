---
title: 'CreateProcessEntryCommon:586: Create process not expected to return'
tags: [problem solution]

category: "Problem Solutions｜WSL"
date: 2023-06-09
---

# CreateProcessEntryCommon:586: Create process not expected to return
## Problem
```bash
$ wsl
Processing fstab with mount -a failed.

<3>WSL (8) ERROR: CreateProcessEntryCommon:370: getpwuid(0) failed 2
<3>WSL (8) ERROR: CreateProcessEntryCommon:374: getpwuid(0) failed 2
<3>WSL (8) ERROR: CreateProcessEntryCommon:577: execvpe /bin/sh failed 2
<3>WSL (8) ERROR: CreateProcessEntryCommon:586: Create process not expected to return
```
<!-- more -->

## Solution
```bash
$ wsl -l
Windows 子系統 Linux 版發佈:
docker-desktop-data (預設)
docker-desktop
Ubuntu-20.04

$ wsl -s Ubuntu-20.04
操作順利完成。
```

## Reference
* [i am getting error on windows subsystem](https://askubuntu.com/questions/1423048/i-am-getting-error-on-windows-subsystem)