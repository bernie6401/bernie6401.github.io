---
title: WSL tty /dev/tty0
tags: [problem solution]

category: "Problem Solutions"
---

# WSL tty /dev/tty0
<!-- more -->

## Problem Description
之前重灌電腦，重新載了WSL，但不知道為甚麼WSL沒有升到version 2，這會導致我在用gdb的時候(我是用gef)，想要設定redirect，但是看了別的視窗的tty都顯示/dev/tty1，而不是/dev/pts/1，導致無法如設定一樣可以分開視窗

## Solution
先回答原因，這是因為目前的wsl version是1而不是2，所以只要把wsl version轉到2就可以了，具體做法可以參考這篇文章[^switch-wsl1-2-wsl2]
1. 確定wsl版本
    ```bash!
    $ wsl --list --verbose
      NAME                   STATE           VERSION
    * Ubuntu-18.04           Stopped         1
      docker-desktop         Stopped         2
      docker-desktop-data    Stopped         2
      Ubuntu-20.04           Running         1
      Ubuntu-22.04           Stopped         1
    ```
    可以看到目前所有版本都還是1
2. Switch
用管理員權限打開PowerShell
    ```shell!
    $ Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform 
    $ wsl --set-version Ubuntu-18.04 2
    $ wsl --set-version Ubuntu-20.04 2
    $ wsl --set-version Ubuntu-22.04 2
    ```
最後就可以開始設定gef config

## Reference
[^switch-wsl1-2-wsl2]:[[WSL] 將 WSL 升級成 WSL2 吧 !](https://samiouob.github.io/2019/06/17/WSL2/)
