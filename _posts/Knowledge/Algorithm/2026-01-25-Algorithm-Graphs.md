---
layout: post
title: "Algorithm-Graphs"
date: 2026-01-25
category: "Knowledge｜Algorithm"
tags: []
draft: false
toc: true
comments: true
---

# Algorithm-Graphs
<!-- more -->
## Terminology
* Graph: 包含$G(V,E)$點到集合$V$ vertices(node)，和有向/無向邊的集合edge $E$，任何binary之間的關係就是Graph(不論有無連結)
* Adjacency List: 是一種紀錄graph上點之間的關係的一種資料結構，詳細可以看[資料結構筆記](https://bernie6401.github.io/Data-Structure-Notes/)

## Elementary Graph Algorithms
### Breadth-First Search(BFS)
下面pseudo code的目的是給一個graph和起始的點s，計算出圖上各個點與s之間的距離

<img src="/assets/posts/Algorithm/BFS-Ex.jpg" alt="" width=300>

* u.d: 代表和起始點s之間的距離
* u.pi: 代表u的上一個
* 利用Queue處理才會有BFS的效果
* Time: $O(V+E)$(Adjacency List)

```c++
BFS(G,s)
// 初始化，全部都是白色且無限大的距離，s本身是灰色且距離是零
for each vertex u inG.V - {s}
    u.color = WHITE // 代表undiscovered
    u.d = ∞
    u.pi = NIL
s.color = GRAY // 代表discovered
s.d = 0
s.pi = NIL
Q = Ø
Enqueue(Q, s)

// 正是計算各點與s的距離
while Q ≠ Ø
    u = Dequeue[Q]
    for each vertex v in G.Adj[u]
        if v.color == WHITE
            v.color = GRAY
            v.d = u.d + 1
            v.pi = u
            Enqueue(Q,v)
    u.color = BLACK // 代表edge的鄰居也被discovered
```

### Depth-First Search(DFS)

```c++
DFS(G)
for each vertex u  G.V
    u.color = WHITE
    u.pi = NIL
time = 0
for each vertex u  G.V
    if u.color == WHITE
        DFS-Visit(G, u)
```

### Topological Sort

### Strongly Connected Component

## Minimum Spanning Trees

## Shortest Paths
### Single Source Shortest Path(SSSP)

### All Pairs Shortest Paths(APSP)

## Maximum Flow