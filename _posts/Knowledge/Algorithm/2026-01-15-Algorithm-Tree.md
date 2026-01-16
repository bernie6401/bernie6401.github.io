---
layout: post
title: "Algorithm-Tree"
date: 2026-01-15
category: "Knowledge｜Algorithm"
tags: []
draft: false
toc: true
comments: true
---

# Algorithm-Tree
這個章節主要在介紹binary-search-tree和紅黑樹的各種操作和演算法實作
<!-- more -->

|Operation|BST|RBT|
|---|---|---|
|Search|$O(h)$|$O(lgn)$|
|Insert|$O(h)$|$O(lgn)$|
|Delete|$O(h)$|$O(lgn)$|
|Minimum|$O(h)$|$O(lgn)$|
|Maximin|$O(h)$|$O(lgn)$|
|Successor|$O(h)$|$O(lgn)$|
|Predecessor|$O(h)$|$O(lgn)$|


## Binary Search Tree(BST)
和前面提到的heap結構不一樣
* BST主要為了「快速搜尋任意值」
* Heap：為了「快速拿到最大值或最小值」

規則：
* 左子樹所有值 < 根
* 右子樹所有值 > 根
* 中序走訪會得到排序結果

### Operation
都可以在$O(h)$的複雜度做到，$h$代表tree的高度
* Search
    ```c++
    Iteratie-Tree-Search(x,k) // x代表目前的點，k代表想找的value
    while x≠NIL and k≠x.key
        if k<x.key
            x = x.left
        else x = x.right
    return x
    ```
* Minimum
* Maximum
* Predecessor(前一個)
* Successor(後一個)
    ```c++
    Tree-Successor(x) // 只要考慮兩種情況

    // 第一種是root本身往右邊找最小的就是successor
    if x.right ≠ NIL
        return Tree-Minimum(x.right)

    // 第二種是children要往上找才能找到successor
    y = x.p
    while y ≠ NIL and x == y.right
        x = y
        y = y.p
    return y
    ```
* Insert
    ```c++
    Tree-Insert(T,z) // z代表要插入的node。分兩種情況，第一種是  插在某個parent底下當作children；第二種是要插入的z本身就是root
    y = NIL
    x = T.root
    while x ≠ NIL
        y = x
        if z.key < x.key
            x = x.left
        else x = x.right
    z.p = y
    if y == NIL
        T.root = z // 屬於要插入的z本身就是Tree的第一個node

    // 以下兩個都是第一種情況，z已經是y的children只是要區分比y大還是小
    else if z.key < y.key
        y.left = z
    else y.right = z
    ```
* Delete:分三種情況
    * node z沒有任何children: 直接刪除
    * node z有一個children: 把z的parent的children pointer改成z的children
    * node z有兩個children: 把z.right中最小的node取代z

    ```c++
    Transplant(T,u,v) // 用v node取代u node
    if u.p == NIL // 代表u已經是root了
        T.root = v
    else if u == u.p.left // u是child且比parent小
        u.p.left = v
    else u.p.right = v // u是child且比parent大
    if v ≠ NIL
        v.p = u.p
    ```
    ```c++
    Tree-Delete(T,z)
    if z.left==NIL // Case A: 只有一個右邊的child
        Transplant(T,z,z.right)
    else if z.right == NIL // Case B: 只有一個左邊的child
        Transplant(T,z,z.left)
    else
        y = Tree-Minimum(z.right)
        if y.p ≠ z // Case D: 有兩個children且可以直接用successor取代z
            Transplant(T,y,y.right)
            y.right = z.right
            y.right.p = y
        Transplant(T,z,y) // Case C,D: 有兩個children且successor就是z.right
        y.left = z.left
        y.left.p = y
    ```

## Red-Black Trees
* 可以保證tree的高度是$O(lgn)$
* 有五個屬性
    1. 每一個node不是紅就是黑
    2. root一定是黑
    3. NIL一定是黑
    4. 如果一個node是紅色，該node的children一定是黑色
    5. 每一個node往下看leaf任意路徑所碰到的黑色node數量會是一樣的
* 這些規則確保樹不會嚴重傾斜(balanced)
* 最多只需要3次rotation就可以保持平衡