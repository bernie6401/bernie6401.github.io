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

|Complexity|Equation|Name|
|---|---|---|
|low|1|Constant|
||$lg(n)$|Logarithmic|
||$\begin{aligned}&=lg^{O(1)}(n)&=(lg(n))^{O(1)}\end{aligned}$|Polylogarithmic|
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

### Merge Sort
* Worst Case: $T(n)=O(nlgn)$

是一種divide-and-conquer的演算法，實作會採用recursive的方式，另外，如果$n$足夠大，就會比Insertion Sort還要好。概念也很簡單，一個unsorted sequence 就切一半，切完的兩半各自再切一半，不斷地切直到各自只有≤2的時候，就開始比較誰大誰小並整合起來

$$
T(n)=\left\{ 
  \begin{array}{r}
    \theta (1), & \text{if $n$ \le c}\ 
    aT(n\over b)+D(n)+C(n),& \text{otherwise}
  \end{array}
\right.
$$