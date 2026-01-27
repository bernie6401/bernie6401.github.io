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
* u.color: 和BFS定義的一樣，分為WHITE, GRAY, BLACK
* u.d: discovery time
* u.f: finishing time
* u.pi: u的predecessor
* Time: $O(V+E)$(adjacency list)

<img src="/assets/posts/Algorithm/DFS-Ex-1.jpg" alt="" width=300>
範例中vertex的兩個數字分別代表u.d/u.f，另外，由於分析到x的地方會跳出recursive loop，則time要再加一

<img src="/assets/posts/Algorithm/DFS-Ex-2.jpg" alt="" width=300>
等到左半邊都分析完了，就會直接跳到w

```c++
DFS(G)
// 初始化graph
for each vertex u  G.V
    u.color = WHITE
    u.pi = NIL
time = 0

// 實際判斷距離
for each vertex u  G.V
    if u.color == WHITE
        DFS-Visit(G, u)
```

```c++
DFS-Visit(G, u)
time = time + 1 // white vertex u has just been discovered
u.d = time
u.color = GRAY
for each vertex v  G.Adj[u] // Explore edge (u,v)
    if v.color == WHITE
        v.pi = u
        DFS-Visit(G, v) // 要用recursive的方法才會有DFS的效果
u.color = BLACK // Blacken u; it is finished
time = time +1
u.f = time
```

#### BFS應用-Lee's Maze Router
* 可以用在IC佈線上: 利用wave propagation的方式，找一個從點S到點T的路徑(在單層single-layer的情況下)
* 優點: 只要路徑存在就一定找的到最快的path
* 缺點: 要是unweighted，且時間和空間複雜度為$O(MN)$太大(在$M\times N$的grid上)

<img src="/assets/posts/Algorithm/Lee's Maze Router.jpg" alt="" width=300>

#### BFS+DFS應用-Soukup's Maze Router
同樣是找點S到點T的path，好處是雖然時間和空間的複雜度和Lee's一樣但卻比前者快10-15倍，不過路徑不一定是最短的

<img src="/assets/posts/Algorithm/Soukup's Maze Router.jpg" alt="" width=300>

* 黑色圓是DFS
* 白色圓是BFS

1. 先看S和T的直線
2. 撞到障礙物就變成黑點
3. 以黑點為原點重新計算距離，直到有一點比黑點更接近T再繼續衝

### Topological Sort
很簡單，是一種對有向無環圖(directed acyclic graph, DAG)的排序方式，把所有頂點排成一個線性順序，使得每一條邊$u\to v$，u 都排在 v 前面。👉 有「先後關係」的排序。
* Time: $O(V+E)$(adjacency list)

```c++
Topological-Sort(G)
call DFS(G) to compute finishing times v.f for each vertex v
as each vertex is finished, insert it onto the front of a linked list
return the linked list of vertices
```

<img src="/assets/posts/Algorithm/Topological -Sort-Ex.jpg" alt="" width=300>

其實就是一路往右排序，每一個task的兩個數字分別代表start time/finish time，結束時間比較早的往右排

### Strongly Connected Component(SCC)
是有向圖中的一個重要概念，在有向圖中，一個頂點集合 $C$，任兩個點 $u,v\in C$ 都滿足$u\to v$ 且 $v\to u$ 都走得到，則 $C$ 是一個 Strongly Connected Component。👉 彼此「來得去、去得回」

* 比較
    |類型|適用圖|條件|
    |---|---|---|
    |Connected Component|無向圖|走得到就算|
    |Strongly Connected Component|有向圖|來回都走得到|

```c++
// 先找誰最後離開圖，再反過來走一次
Strongly-Connected-Components(G)
call DFS(G) to compute finishing times u.f for each vertex u // 利用DFS找出圖上的vertices 的finish time(u.f)
compute G_Transpose // 把圖反向
call DFS(G_Transpose), but in the main loop of DFS, consider the vertices in order of decreasing u.f (as computed in line 1) // 從最後一個推回來
output the vertices of each tree in the depth-first forest of step 3 as a separate strongly connected component
```
* $G^T=(V,E^T)$: G的Transpose，$E^T=\{(u,v):(v,u)\in E\}
* Time: $O(V+E)$(adjacency list)

## Minimum Spanning Trees(MST)
* Spanning Tree(生成樹): 用 $V-1$ 條邊連通所有 $V$ 個頂點且無 cycle
* Edge Count: $\mid E_{MST}\mid = V-1$
* Cut Property(切割性質): 對任意切割$(S,V-S)$(其實就是分成兩個群)，跨越該 cut 的最小權重邊，一定存在於某棵 MST 中
    * Crossing edge：跨越 cut 的邊
    * Light edge：跨越該 cut 的最小權重邊

    <img src="/assets/posts/Algorithm/MST-Cut-Edge.jpg" alt="" width=300>
    * 有被虛線切到的就是cut edge
* Input: 無向的graph $G=(V,E)$，有權重的edge
* Objective: 目的是找到能夠連結所有vertices但又最短的path
* 應用
    * circuit interconnection(minimizing tree radius): 連接所有 pin，線長 ≈ 成本 👉 先用 MST 降低總線長，再做優化
    * communication network(minimize tree diameter): 城市要鋪光纖、公司內部拉網路、水管、電線、油管，節點是地點，邊等於鋪設成本 👉 MST = 最便宜的整體鋪設方案

```c++
Generic-MST(G,w)
A = ∅
while A does not form a spanning tree
    find an edge (u,v) that is safe for A
    A = A ∪ {(u,v)}
return A
```

### 實作
||Kruskal|Prim|
|---|---|---|
|觀點|邊|點|
|資料結構|Union-Find|Priority Queue|
|適合|稀疏圖|稠密圖|
|是否需要連通|否（變森林）|是|

#### Kruskal's
* Time: $O(ElgE+V)$

<img src="/assets/posts/Algorithm/MST-Kruskal-Ex.jpg" alt="" width=300>

```c++
MST-Kruskal(G,w)
A = Ø
for each vertex v in G.V
    Make-Set(v)
sort the edges of G.E by nondecreasing weight w // 由小到大排序
for each edge (u,v) in G.E, in order by nondecreasing weight // 從weight最低的開始
    if Find-Set(u)  Find-Set(v)
        A = A  {(u, v)}
        Union(u,v)
return A
```

#### Prim-Dijkstra's

<img src="/assets/posts/Algorithm/MST-Prim-Dijkstra-Ex.jpg" alt="" width=300>

```c++
MST-Prim(G,w,r)
// Q: priority queue for vertices not in the tree, based on key.
// key: min weight of any edge connecting to a vertex in the tree.
for each vertex u in G.V
    u.key = ∞
    u.pi = NIL
r.key = 0
Q = G.V
while Q  
    u = Extract-Min(Q)
    for each vertex v in G.Adj[u]
        if v in Q and w(u,v) < v.key
            v.pi = u
            v.key = w(u,v)
```

## Shortest Paths
### Single Source Shortest Path(SSSP)

### All Pairs Shortest Paths(APSP)

## Maximum Flow