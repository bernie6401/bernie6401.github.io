---
layout: post
title: "Windows Context Menu Customization"
date: 2026-02-24
category: "Tutorial｜Others"
tags: []
draft: false
toc: true
comments: true
---

# Windows Context Menu Customization
<!-- more -->

## Purpose
我想要達成右鍵選單可以直接執行某個bat或script

## Steps
1. 開啟rededit
2. 到`電腦\HKEY_CLASSES_ROOT\Directory\Background\shell\`新增機碼，名字可以隨便取
3. 新增名為command的機碼
3. 新增名為Icon的字串值並設定value為ico的path
4. (Optional)新增名為HasLUAShield的字串值，不需要設定value
5. 點進command後設定value為要啟動的執行檔或bat檔案的path

## Script
```reg
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\Background\shell\<ContextMenuName>]
@="<ContextMenuName>"
"Icon"="<path to ico>"
"HasLUAShield"=""

[HKEY_CLASSES_ROOT\Directory\Background\shell\<ContextMenuName>\command]
@="\"<path to exe/bat file with double ba>\""
```