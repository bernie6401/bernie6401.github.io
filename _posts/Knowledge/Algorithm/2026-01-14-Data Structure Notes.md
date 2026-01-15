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

|Operation|Heap Method|Array Method在sorted array下(很花時間)|
|---|---|---|
|INSERT|$O(lgn)$: 直接插在最後並做fix heap的動作|$O(n)$: 每一個要往後|
|MAXIMUM|$O(1)$: 直接read第一個|$O(1)$: 直接read第一個|
|EXTRACT-MAX|$O(lgn)$: 直接刪除第一個元素並用最後一個取代再做heapify|$O(n)$: 每一個要往後|
|INCREASE-KEY|$O(lgn)$: 從target遍歷一個適當的地方插入新的key|$O(n)$: 每一個要往前|
