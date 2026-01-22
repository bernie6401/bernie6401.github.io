---
layout: post
title: "Algorithm-Greedy Algorithm"
date: 2026-01-22
category: "Knowledge｜Algorithm"
tags: []
draft: false
toc: true
comments: true
---

# Algorithm-Greedy Algorithm
<!-- more -->
* <span style="background-color: yellow">總是會做出當下看起來最佳的選擇</span>
* 和Heuristic(經驗法則)的差別是Greedy Algorithm可以找到最佳解
* Vortex Cover的例子可以直接看講義

## Activity-Selection Problem(排程問題)
想像成CPU的工作
* Input: 
    * $S={1,2,...,n}$ activity的集合
    * 該集合包含activity $i$的開始時間$s_i$和結束時間$f_i$
* Objective: 在一個人（或資源）一次只能做一個活動且兩個活動**不重疊**才能同時被選的條件下，<span style="background-color: yellow"></span>選出最多個彼此不衝突的活動

### 用Greedy的方式解
1. 先排序結束時間$f_i$，由小到大
2. 選擇第一個activity
3. 往下選，只要下一個activity的$s_i\le f_j$就選，$j$代表最近選擇的activity

```c++
Greedy-Activity-Selector(s,f)
// Assume f1≤f2≤…≤fn.
n = s.length
A = {1}
j = 1
for i = 2 to n
    if s[i] ≥ f[j]
        A = A ⋃ {i}
        j = i
return A
```