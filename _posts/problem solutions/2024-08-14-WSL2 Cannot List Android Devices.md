---
title: WSL2 Cannot List Android Devices
tags: [problem solution]

category: "Problem Solutions"
---

# WSL2 Cannot List Android Devices

## 問題描述
這個問題的前題是Windows CMD以及WSL2都有正確安裝adb，但前者可以正常list出連接的device，後者卻為空

## How to Solve
這是參考[StackOverflow - ADB device list empty using WSL2](https://stackoverflow.com/a/71414575/15036381)的說明，具體原理就是我們直接把Windows安裝adb的path，soft link給WSL2的path就可以了
1. 先找出Windows安裝adb的path
    自行尋找
2. 找出WSL2中adb的path
    通常是`/usr/bin/adb`
    ```bash
    $ ll /usr/bin/adb
    lrwxrwxrwx 1 root root 45 Aug 14 12:07 /usr/bin/adb -> lrwxrwxrwx 1 root root 37 Jan 23  2022 /usr/bin/adb_bk -> ../lib/android-sdk/platform-tools/adb
    ```
3. 備份原本的soft link
    ```bash
    $ sudo mv /usr/bin/adb /usr/bin/adb_bk
    ```
4. 取代softlink
    ```bash
    $ sudo ln -sf /mnt/<folder path to adb>/adb.exe /usr/bin/adb
    ```
5. 測試
    ```bash
    $ adb devices
    * daemon not running; starting now at tcp:5037
    * daemon started successfully
    List of devices attached
    RFCW81CY9AD     device
    ```