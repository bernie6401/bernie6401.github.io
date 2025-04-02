---
title: Unexpected fatal error while initializing python runtime.
tags: [problem solution]

---

# Unexpected fatal error while initializing python runtime.
Complete error message: Unexpected fatal error while initializing python runtime. Please run idapyswitch to confirm or change the used Python runtime

## Solution
[IDA出错unexpected fatal error while intitailizing python runtime.](https://zhuanlan.zhihu.com/p/434575474)
1. 只要在使用者變數增加`PYTHON:C:\Users\berni\anaconda3\envs\NTUCNS\`
![](https://hackmd.io/_uploads/r1aVq-su2.png)

2. 在增加環境變數`C:\Users\berni\anaconda3\envs\NTUCNS\Lib`
![](https://hackmd.io/_uploads/Hkkv5bs_2.png)

Note: ==但這樣的情況會變成VSCode的terminal沒辦法使用conda的command，而一般的CMD或是WSL不受影響==

## IDA Pro 7.7
[IDA Pro 7.7](https://github.com/751643992/IDA_Pro_7.7)

## Other Reference
[IDA免安裝版沒有python執行功能](https://blog.csdn.net/tbk345/article/details/124163684)
[IDA7.0的脚本语言：idc和idapython](https://blog.csdn.net/weixin_45055269/article/details/105940348)