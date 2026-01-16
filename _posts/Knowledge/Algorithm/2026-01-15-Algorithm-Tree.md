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
<!-- more -->

## Tree
### Binary Search Tree(BST)
和前面提到的heap結構不一樣
* BST主要為了「快速搜尋任意值」
* Heap：為了「快速拿到最大值或最小值」

規則：
* 左子樹所有值 < 根
* 右子樹所有值 > 根
* 中序走訪會得到排序結果

#### Operation
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
* Delete

### Red-Black Trees