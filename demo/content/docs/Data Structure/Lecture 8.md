---
title: Lecture 8
tags: [Data Structure, NYCU]

---

# Lecture 8
###### tags: `Data Structure` `NYCU`

## Reference & Background
[Lec08 資料結構 第五週課程](https://youtu.be/lhXHk8IuFeQ)
[C語言: 超好懂的指標，初學者請進～](https://kopu.chat/c%E8%AA%9E%E8%A8%80-%E8%B6%85%E5%A5%BD%E6%87%82%E7%9A%84%E6%8C%87%E6%A8%99%EF%BC%8C%E5%88%9D%E5%AD%B8%E8%80%85%E8%AB%8B%E9%80%B2%EF%BD%9E/)

## Note
### Rewind
* Array
之前提到Array的結構，其缺點是大小是固定的，但有時候需要儲存的東西可能是動態改變的，且沒有用到的空間就會變成一種浪費
* Solution
此時就可能可以考慮用Link-List的結構處理這樣的資料


### Link-List
* 主要結構
每一個Element都會有兩個儲存單位，一個是儲存資料本體，另一個是儲存pointer，指向下一個Element的位置
![](https://hackmd.io/_uploads/SJ0yRNXH3.png)

* Insert `GAT`
Create新的node，儲存`GAT`，並改變前後的指標，原本`FAT`的指標要assign給`GAT`的pointer，然後`GAT`的位址也要assign給`FAT`
![](https://hackmd.io/_uploads/H1JrREXBh.png)

* Delete `GAT`
把`HAT`的位址assign給`FAT`
![](https://hackmd.io/_uploads/SJ2zkr7B3.png)
    * 缺點：如果要delete某一個Element就需要"先找到該Element的位置在哪裡"，如果Link-List 很長，則要做到這件事情的Overhead就會很高
    * Solution: Double-Link-List，可以從前後同時找要刪除的Element，這樣的話就會比較快

#### Implement
:::spoiler Source Code - Composite Classes
```cpp!
class ThreeLetterList; // forward delcanon 
class ThreeLetterNode {
    friend class ThreeLetterList; 
    private 
    char data[3]; // 每一個Elment就是只有儲存三個字元
    ThreeLetterNode *link;
};

class ThreeLetterList{ 
    public: 
        // List Manipulat10n operabons 
    private:
        ThreeLetterNode *first;
};
```
:::

:::spoiler Another Implementation - Nested Classes
```cpp!
class ThreeLetterList{
    public:
    // List ManipuIation operatlons 
    private:
        class ThreeLetterNode{ // nested class 
        public:
            char data[3]; 
            ThreeLetterNode *link;
        };
        ThreeLetterNode *first;
};
```
:::

* How to create 2 link-list element
    :::spoiler Example Code
    ```cpp!
    void List::Create2()
    {
        /* create a linked list with two nodes */ 
        first = new ListNode(10); 
        first->link = new ListNode(20); 
    }
    ListNode::ListNode(int element=0)
    {
        data = element; 
        link = 0;
    }
    ```
    :::
    ![](https://hackmd.io/_uploads/By5RniQSh.png)

* How to insert 50 in a existed link-list
    :::spoiler Example Code
    ```cpp!
    void List::Insert50 (ListNode *x)
    {
        /* insert a new node with data=50 into the list* */ 
        ListNode *t = new ListNode(50); 
        if (!first) 
        {
            first = t; 
            return;
        }
        //insert after x 
        t->link = x->link; 
        x->link = t;
    }
    ```
    :::
    ![](https://hackmd.io/_uploads/B1nW2imHh.png)