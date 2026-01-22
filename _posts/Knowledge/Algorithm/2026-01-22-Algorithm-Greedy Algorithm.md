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