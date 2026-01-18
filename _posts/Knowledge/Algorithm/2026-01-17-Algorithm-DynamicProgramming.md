---
layout: post
title: "Algorithm-Dynamic Programming"
date: 2026-01-17
category: "Knowledge｜Algorithm"
tags: []
draft: false
toc: true
comments: true
---

# Algorithm-Dynamic Programming
<!-- more -->
* Divide-and-Conquer： 子問題彼此獨立、不重複
* Dynamic Programming： 子問題會重複出現，要記下來避免重算
* 使用DP的時機: 線性的排序法 + 無法重新排列
    * Linear assembly lines
    * matrices in a chain
    * characters in a string
    * points around the boundary of a polygon
    * points on a line/circle
    * the left to right order of leaves in a search tree
    * ...
* 在DP問題中，subproblem的最佳解不見得是overall的最佳解
* DP問題可以直接畫表格的方式，用簡單的計算就知道哪一個solution是optimal(Tabular Method)

| 面向     | Divide-and-Conquer | Dynamic Programming                 |
| ------ | ------------------ | ----------------------------------- |
| 子問題關係  | **彼此獨立**           | **大量重疊**                            |
| 是否記憶結果 | ❌ 不需要              | ✅ 必須（memo / table）                  |
| 典型技術   | Recursion          | Recursion + Memoization 或 Iteration |
| 時間優化關鍵 | 問題切得平均             | 避免重複計算                              |
| 思考重點   | 怎麼「分」              | 狀態如何「轉移」                            |

## Assembly-line Scheduling
* Shortest Path Algorithm也是需要DP的觀念
* 只要記得最短路徑這個最佳解就好，其他路徑不重要

### 車子組裝生產線例子
<img src="/assets/posts/Algorithm/Assembly-line Scheduling Example.png" width=300>

* Objective: 在例子中，找一個生產線的走法，使時間成本更少
    * 可以轉換生產線，但要付出時間成本$t_{i,j}$ → $i$代表生產線，$j$代表需要的station
* Worst Case: $\Omega (2^n)$: 暴力法

### 解法
要找到$S_{1,n}$之前的最佳解，需要從入口到$S_{1,n-1}$之前的最佳解，把之前的路徑用divide and conquer解就可以了。
* $f_i[j]$代表從起點到$S_{i,j}$最短的時間，目前先考慮第一條生產線，如果$j$只有一個那就只有一種走法；大於兩條之後，可以考慮換生產線，當然要加上轉換的時間，這個是用table的方式呈現，分別紀錄$f_{1,1},f_{1,2},f_{1,3},...,f_{1,n}$和$f_{2,1},f_{2,2},f_{2,3},...,f_{2,n}$分別是多少，以本例子來說是一個2*n的table size
$$
f_i[j] = \left\{
\begin{array}{l}
   e_1 + a_{1,1}, \text{if} j = 1 \\
   min(f_1[j-1] + a_1,j,f_2[j-1] + t_{2,j-1} + a_{1,j}), \text{if} j \ge 2
\end{array}
\right.
$$

<img src="/assets/posts/Algorithm/DP-Assembly-line-Scheduling-Fastest-Way-Psuedo Code.png" width=300>
* asterisk symbol代表optimal solution
* 前面的$f$已經紀錄到$S_{i,j}$的最短路徑是多少，可是到底是從哪一條生產線來的不知道，所以需要另外一個table來紀錄，這就是$I$這個table存在的目的，大小是x*(n-1)

## Matrix-chain subsequence (矩陣相乘以及相乘的順序)
* $A$是$pxq$ matrix；$B$是$qxr$ matrix；$C=AB$是$pxr$: $C[i,j]=\sum\limits_{k = 1}^q{A[i,k]B[k,j]}$
* Time Complexity: $O(pqr)$

```c++
Matrix-Multiply(A, B)
if A.columns ≠ B.rows
    error "incompatible dimensions" // 先檢查相乘的矩陣維度是否valid
else let C be a new A.rows * B.columns matrix
    for i = 1 to A.rows
        for j = 1 to B.columns
            c_ij = 0
            for k = 1 to A.columns
                c_ij = c_ij + a_ikb_kj
    return C
```

### 3個矩陣以上就會有順序的問題
* Objective: 使乘法數量越少越好
* 例子: $A_1$: 4x2;$A_1$: 2x6;$A_3$: 5x1
    * $(A_1A_2)A_3$: $4*2*5+4*5*1=60$
    * $A_1(A_2A_3)$: $2*5*1+4*2*1=18$
* 問題: 要怎麼知道一個Matrix-Chain怎麼乘會讓乘法的operations數量最少?
    * BruteForce: $P(n)$代表$n$個矩陣相乘的方法有多少種，$\Omega({{4^n}\over {n^3/2}})$
        $$
        P(n) = \left\{
        \begin{array}{l}
        1, \text{if} n = 1 \\
        \sum\limits_{k=1}^{n-1}{P(k)P(n-k)}, \text{if} n \ge 2
        \end{array}
        \right.
        $$
    * 因為matrix chain是linearly ordered並且不能rearranged(每一種矩陣都要存在並且順序不能被改變)，所以可以使用DP

## Longest Common Subsequence
可以拿來做DNA比對

## Optimal binary search trees

## Maximum planar subset of chords
