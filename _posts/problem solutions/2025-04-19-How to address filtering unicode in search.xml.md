---
layout: post
title: "How to address filtering unicode in search.xml"
date: 2025-04-19
category: "Problem Solutions"
tags: []
draft: false
toc: true
comments: true
---

# How to address filtering unicode in search.xml
最主要發現這個問題是因為我想要在網站中enable搜尋的功能，但每次都只有等待的迴圈icon，我以為是我的posts數量太多，需要做很多的初始化，後來使用Google Search Console之後才知道有一個search.xml的文件，裡面是所有文章的title, content, category, tags等東西，詳細訪問`http://localhost:4000/search.xml`後才發現，原來是這邊出現問題
![](/assets/posts/螢幕擷取畫面 2025-04-19 175517.png)
<!-- more -->

## Problem Statement
![](/assets/posts/螢幕擷取畫面 2025-04-19 175937.png)
從上圖可以知道有一些東西在search.xml中無法被parse，詳細看了之後發現問題全部出現在那些應該是unicode的字元
![](/assets/posts/螢幕擷取畫面 2025-04-19 180042.png)
照理說把那些字元刪除就可以了，所以我直接replace有出現的四個字元，`<0x01><0x10><0x14><0x1b>`

## Solutions
只要把search.xml中的語法改進就可以了
{% gist 46dab97bec8191a067200407aa1f9030 %}

## Result
最後只要看browser能不能夠正確parse search.xml就可以了，在網站上的sarch功能也可以正常使用