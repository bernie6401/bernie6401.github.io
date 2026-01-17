---
title: LeetCode - Two Sum
tags: [LeetCode, Easy]

category: "LeetCode｜Easy"
date: 2024-01-31
---

# LeetCode - Two Sum
<!-- more -->

## Recon & Description
:::spoiler Description
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

 

Example 1:
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```
Example 2:
```
Input: nums = [3,2,4], target = 6
Output: [1,2]
```
Example 3:
```
Input: nums = [3,3], target = 6
Output: [0,1]
```
:::
簡單來說就是回傳一個list，包含兩個element，也就是原本nums的index位置，對應的兩個數值相會等於target，就這樣，不過他給的test case算蠻佛心的，可以更完善原本沒有想到的exception

## PoC
重要的事情是list變數不能直接assign，因為記憶體是一樣的，詳細可以參考[^python_list_nee_2_know]，之前就有發生過這個問題，這次是詳細的閱讀底層的說明，另外我覺得我有一點把poc弄得太複雜了，畢竟要考慮的東西頗多，就先不管一些complexity的optimization
```python=
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        result = []
        tmp_list = list(nums)
        for i in range(len(nums)):
            tmp_list.pop(0)
            if (target - nums[i]) in tmp_list:
                result.append(i)
                result.append(self.find(nums, target, i))
                return result
            else:
                pass

    def find(self, nums, target, j):
        for i in range(j+1, len(nums)):
            if target - nums[i] == nums[j]:
                return i
            else:
                pass
```

## Result
![](https://hackmd.io/_uploads/ryzB3YAs2.png)
看來還有很多進步的空間，不過就先這樣ㄅ

## Reference
[^python_list_nee_2_know]:[[Python] 關於變數與參考的二三事 ](https://skylinelimit.blogspot.com/2018/04/python-variable-reference.html)