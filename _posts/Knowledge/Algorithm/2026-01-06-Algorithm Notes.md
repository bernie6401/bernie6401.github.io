---
layout: post
title: "Algorithm Notes"
date: 2026-01-06
category: "Knowledge｜Algorithm"
tags: []
draft: false
toc: true
comments: true
---

# Algorithm Notes
<!-- more -->
## Terminology
* $O$: upper bound function(worse case)
* $\Omega$: lower bound function(best Case)
* $\theta$
* In-place: 演算法實作中會用到的變數數量與記憶體大小都是constant；另一個解釋是如果演算法在運作時，主要直接在原本的資料結構上操作，就稱為 in-place。
* Stable: 如果排序前後，具有相同 key 的元素，其相對順序不會改變，就稱這個排序是 stable（穩定） 的。

|Complexity|Equation|Type|
|---|---|---|
|low|1|Constant|
||$lg(n)$|Logarithmic|
||$lg^{O(1)}(n)$|Polylogarithmic|
||$lg(n)^{O(1)}$|Polylogarithmic|
||$\sqrt(n)$|Sublinear|
||$n$|Linear|
||$nlg(n)$|Loglinear|
||$n^2$|Quatratic|
||$n^3$|Cubic|
||$n^4$|Quartic|
||$2^n,3^n,...$|Exponential|
||$n!$|Factorial|
|high|$n^n$|-|


## 如何找Recurrence類型演算法的$T(n)$
1. Iteration: 就利用展開、整理、展開、整理，找出規律統合起來，就是傳統的方法
2. Substitution(Guess &Verify): 老師說是個高深的方法
3. Master Theorem: 背公式的方法，在一些條件下可以直接找出worst case