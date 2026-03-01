---
title: "Unexpected fatal error while initializing python runtime"
tags: [problem solution]

category: "Problem Solutions｜Others"
date: 2024-01-31
---

# Unexpected fatal error while initializing python runtime
Complete error message: Unexpected fatal error while initializing python runtime. Please run idapyswitch to confirm or change the used Python runtime
<!-- more -->

## Solution
[IDA出错unexpected fatal error while intitailizing python runtime.](https://zhuanlan.zhihu.com/p/434575474)
1. 只要在使用者變數增加`PYTHON:C:\Users\berni\anaconda3\envs\NTUCNS\`
    ![](https://hackmd.io/_uploads/r1aVq-su2.png)
2. 在增加環境變數`C:\Users\berni\anaconda3\envs\NTUCNS\Lib`
    ![](https://hackmd.io/_uploads/Hkkv5bs_2.png)

Note: <span style="background-color: yellow">但這樣的情況會變成VSCode的terminal沒辦法使用conda的command，而一般的CMD或是WSL不受影響</span>

## IDA Pro 7.7
[IDA Pro 7.7](https://github.com/751643992/IDA_Pro_7.7)

## 要如何在IDA中使用python
有鑑於之前查找的諸多資料，要在IDA中使用python又不能出現上述問題，還要讓vscode/CMD能夠正常使用conda，只有目前這一個方法，那就是install一個獨立於conda的[python環境](https://www.python.org/downloads/windows/)(我是安裝py3.9/windows)，並且不要設定環境變數，也就是在安裝的時候environment path的地方不要勾選，然後也不要在environment path的地方設定`PYTHONHOME`，接著用ida中的`idapyswitch`指定安裝的python環境即可，接下來就可以自己安裝ida plugins會用到的python library
```bash
$ C:\path\to\python.exe -m pip install --upgrade pip
$ C:\path\to\python.exe -m pip install keystone-engine yara-python
```

## Other Reference
* [IDA免安裝版沒有python執行功能](https://blog.csdn.net/tbk345/article/details/124163684)
* [IDA7.0的脚本语言：idc和idapython](https://blog.csdn.net/weixin_45055269/article/details/105940348)