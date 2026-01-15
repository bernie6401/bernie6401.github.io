---
layout: post
title: "Data Structure Notes"
date: 2026-01-14
category: "Knowledge｜Algorithm"
tags: []
draft: false
toc: true
comments: true
---

# Data Structure Notes
<!-- more -->

## Max Heap
是一種binary tree結構，root一定會比leaf還要大，只要符合這個結構就是max-heap

適合用在實現Priority Queue資料結構以及HeapSort演算法

## Priority Queue
需要滿足四種不同的operation
1. INSERT(S,x): 把key x插入到S集合
2. MAXIMUM(S): return集合中最大的key
3. EXTRACT-MAX(S): return & remove集合中最大的key
4. INCREASE-KEY(S, x, k): 將x的key增加到k

|Operation|Heap Method|Array Method|
|---|---|---|
|INSERT|$O(lgn)$|$O(n)$|
|MAXIMUM|$O(1)$|$O(n)$|
|EXTRACT-MAX|$O(lgn)$|$O(n)$|
|INCREASE-KEY|$O(lgn)$|-|
