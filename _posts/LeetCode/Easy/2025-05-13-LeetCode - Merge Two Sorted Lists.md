---
layout: post
title: "Merge Two Sorted Lists"
date: 2025-05-13
category: "LeetCode/Easy"
tags: []
draft: false
toc: true
comments: true
---

# Merge Two Sorted Lists
You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists into one **sorted** list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.
**Example 1:**
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

**Example 2:**
Input: list1 = [], list2 = []
Output: []

**Example 3:**
Input: list1 = [], list2 = [0]
Output: [0]

**Constraints:**
* The number of nodes in both lists is in the range `[0, 50]`.
* `-100 <= Node.val <= 100`
* Both `list1` and `list2` are sorted in non-decreasing order.

<!-- more -->
## Recon & Description
我自己嘗試幾種方式，一開始我以為可以不需要考慮他的結構，畢竟在Description的地方所使用的test case也只是一般的list，因此我一開始考慮的解法就是直覺的list相加再sorted，但最後測試會出error，索性換另一個想法，既然test case一定會single linked-list，那我可不可以直接把value提取出來變成一般的list後相加再sorted，像前面那樣，只是一開始和最後需要轉換罷了，但最後線上測試也是出error，想來想去也沒有什麼好的想法，就看其他網友的解法，會常常看到其中一種解法是dummy linked-list，這個方式我並不喜歡，因為這算是運用python上的一個語言的特性，所以我想不到，但理解發生甚麼事，所以找了其他我可以接受後續也可以implement的做法，其實就是recursive的方式，異常簡單

## PoC
```python
from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        while list1 and list2:
            if list1.val < list2.val:
                list1.next = self.mergeTwoLists(list1.next, list2)
                return list1
            else:
                list2.next = self.mergeTwoLists(list1, list2.next)
                return list2
            
        return list1 if list1 else list2

if __name__ == "__main__":
    # Example usage:
    list1 = ListNode(1, ListNode(2, ListNode(4)))
    list2 = ListNode(1, ListNode(3, ListNode(4)))
    
    solution = Solution()
    merged_list = solution.mergeTwoLists(list1, list2)
    
    # Print merged list
    while merged_list:
        print(merged_list.val, end=" -> ")
        merged_list = merged_list.next
    print("None")
```

## Result
![](/assets/posts/螢幕擷取畫面 2025-05-14 105731.png)