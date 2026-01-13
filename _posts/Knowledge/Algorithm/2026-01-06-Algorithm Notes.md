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
* $\theta$: 

|Complexity|Equation|Name|
|---|---|---|
|low|1|Constant|
||$lg(n)$|Logarithmic|
||$lg^{O(1)}(n)=(lg(n))^{O(1)}$|Polylogarithmic|
||$\sqrt(n)$|Sublinear|
||$n$|Linear|
||$nlg(n)$|Loglinear|
||$n^2$|Quatratic|
||$n^3$|Cubic|
||$n^4$|Quartic|
||$2^n,3^n,...$|Exponential|
||$n!$|Factorial|
|high|$n^n$|-|


## Sorting
### Insertion sort
* Input: 亂序的sequence
* Output: 正序的sequence
* Worst Case: Linear $\to T(n) = n^2 \to$ input原本就是reverse sorted order
* Best Case: Quadratic $\to T(n) = n \to$ input原本就是sorted order

可以想像成把sequence分成兩邊，左邊是已經排序好的，右邊是正要排序，第一個element預設已經排序好，所以從第二個element開始，先把要排序的element保留住(key)，並且左邊所有element只要比key還大就往右邊移動，這樣就可以把key放在正確的位置

```c++
InsertionSort(A)
for j = 2 to A.length do
    key = A[j]
    I =j - 1

```