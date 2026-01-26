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

## Tree
分成Full/Complete/Perfect/Skewed四種
* Full代表每一個node都有0或2個children
* Complete代表d-1 level都是滿的
* Perfect代表所有node都有2個children
* Skewed代表所有node都只有一個children(非常unbalanced)

結構如下，正常的complete binary tree用array不會浪費，但如果是skewed就超浪費，所以可以用pointer
```c++
struct_node{
    int key_value;
    node *parent;
    node *left;
    node *right;
}
```

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

## Disjoint Set
用來快速判斷 兩個元素是不是在同一個集合，以及把 兩個集合合併。
### Terminology
* Set:集合，$S_1,S_2,...,S_k$
* Collection: a family of sets，$S=\{S_1,...,S_k\}$
* Representative: 一個set中類似班長的角色，也判斷兩個集合是不是有關聯就要看他們的representative是不是一樣的

### 支援的操作
* Make-Set(x): S_x=\{x\}$，把某一個元素自成一個集合
* Union(x,y): $S_x\cup S_y$
* Find-Set(x): 找有含x的集合的班長是誰

### Example
<img src=/assets/posts/Algorithm/DISJOINT-SET-EXAMPLE.jpg" alt="" width=300>