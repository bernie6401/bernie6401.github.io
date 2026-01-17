---
title: LeetCode - Valid Parentheses
tags: [LeetCode, Easy]

category: "LeetCode｜Easy"
date: 2024-01-31
---

# LeetCode - Valid Parentheses
<!-- more -->

## Recon & Description
:::spoiler Description
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

    Open brackets must be closed by the same type of brackets.
    Open brackets must be closed in the correct order.
    Every close bracket has a corresponding open bracket of the same type.

 

Example 1:
```
Input: s = "()"
Output: true
```
Example 2:
```
Input: s = "()[]{}"
Output: true
```
Example 3:
```
Input: s = "(]"
Output: false
```
:::
這一題非常簡單，就只是分辨輸入進來的括號有沒有符合使用的設定，也就是正確的配對小中大括號彼此對應這樣，一開始用了第一種方法(付在下面)發現coverage很低，所以就想第二種方法比較符合正確的實作，所以分數也比較高

## PoC
```python!
right_brackets = ['(', '[', '{']
left_brackets = [')', ']', '}']
brackets_dic = {"(":0, ")":0, '[':1, ']':1, '{':2, '}':2}


class Solution:
    def isValid(self, s: str) -> bool:
        right = []
        left = []
        brackets_stack = []
        first_situation = 0
        second_situation = 0
        if len(s) % 2 != 0:
            return False
        
        '''################
        Method 2
        ################'''
        for i in range(len(s)):
            if s[i] in right_brackets:
                brackets_stack.append(s[i])
                continue
            else:
                try:
                    if brackets_dic[s[i]] == brackets_dic[brackets_stack[-1]]:
                        brackets_stack.pop()
                        continue
                    else:
                        return False
                except:
                    return False
        if brackets_stack == []:
            return True
        else:
            return False
    
result = Solution()
test_case = ["){", "()", "()[]{}", "(]", "{[]}", "([)]"]
print(result.isValid(test_case[0]))
```

:::spoiler Method 1
```python!
right_brackets = ['(', '[', '{']
left_brackets = [')', ']', '}']
brackets_dic = {"(":0, ")":0, '[':1, ']':1, '{':2, '}':2}


class Solution:
    def isValid(self, s: str) -> bool:
        right = []
        left = []
        first_situation = 0
        second_situation = 0
        if len(s) % 2 != 0:
            return False
        '''################
        Method 1
        ################'''
        '''
        for i in range(len(s)):
            if s[i] in right_brackets:
                right.append(s[i])
                continue
            if s[i] in left_brackets:
                left.append(s[i])
                continue
        if len(right)  != len(left):
            return False
        else:
            for i in range(len(left)):
                if brackets_dic[right[i]] == brackets_dic[left[i]]:
                    first_situation += 1
                    pass
            
                elif brackets_dic[right[i]] == brackets_dic[left[len(left) - i - 1]]:
                    second_situation += 1
                else:
                    return False
            if first_situation == len(left) or second_situation == len(left):
                return True
            else:
                return False
        '''
```
:::

## Result
![](https://hackmd.io/_uploads/BJgRaNb3n.png)