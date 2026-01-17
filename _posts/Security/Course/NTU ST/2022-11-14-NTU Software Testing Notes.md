---
title: NTU Software Testing Notes
tags: [NTU_ST, Software Testing, NTU]

category: "Security｜Course｜NTU ST"
date: 2022-11-14
---

# NTU Software Testing Notes
<!-- more -->
###### tags: `NTU_ST` `Software Testing`
**All content in this presentation is refer to [Pro. Farn Wang Website](http://cc.ee.ntu.edu.tw/~farn/courses/ST/2021.Spring/)**

:::spoiler Click to open TOC
[TOC]
:::

# 2.5 Graph Coverage for Specifications

## Design Spec.
* What is design specification?
    * 描述軟體應該有的行為(可見或不可見都有可能)
* What is different between requirement and specification
    * requirement: 顧客端 / specification: 技術端
* Sequence就是一連串的行為和狀態->script
* Testing就是在看script有發生該發生的事情
* Two types of description are used in this chapter
    * **Sequencing constraints**
    * **State behavior**

## Sequencing constraints
* Constraint有可能是document的一些潛規則或是method上順序的限制，e.g. stack data structure在沒有push前不能pop
* Queue Example: precondiction就是這個例子的sequence constraint
![Queue Example](https://i.imgur.com/3RaZRfK.png)
* File ADT Example
    * ADT: Abstract Data Type其實就是早期的class
    * sequence constraint about example
    1. 寫之前要先打開file
    2. 關閉之前要先打開file
    3. 在close file之後除非再open file，不然不可以write file
    4. close file前一定要write file，不然就浪費這個procedure
    ![File ADT Example](https://imgur.com/1NYVCj1.png)
    * Static Checking: 先不跑test input，先針對畫出來的graph做checking
    * [1, 3, 4, 6]就是這個instance的open到close之間沒有任何的write procedure
    * Edge[1, 3]和Edge[3, 4]可能有共同變數在控制file的read、write，讓file不會經過Edge-Pair[1, 3, 4]->實際上會不會發生還是要看中間的邏輯
    * Testing的目的是要找出所有可能會違反test constraint或其他條件使software不正常運作

    * Test Requirements for FileADT
        1. 有write但沒open
        2. 有close但沒open
        3. close當中再包含write
        4. close-open中無任何write
    * 如果program的設計與邏輯都正確，所有test requirements都**不可執行**

## State behavior
* FSM: finite state machine(有限狀態機)是個用來描述軟體狀態在執行時變換的圖
* FSM不太適合用在狀態很多的program
    * **Nodes**: States / **Edges**: Transitions
    ![FSM](https://imgur.com/lrhkWRO.png)
    * FSM Example
        ![FSM Example](https://imgur.com/APKr4h7.png)
        * 上圖是指海上熱帶氣旋和颱風之間的關係
        * 列在FSM的變數，都是會影響state轉換的variable
    * Application
        * **Embedded** System and control software
        * **Abstract data types**
        * **Compiler** and operating systems
        * **Web** application
    * **Language** for describing FSM
        * UML Statecharts: 比較複雜，因為state中還可以再包state
        * Automata: 和FSM最相關
        * State tables(SCR)
        * Petri nets: 和FSM有很多差異
    * Annotations on FSM
        ![Annotations Example](https://imgur.com/xrKh1rS.png)
        * **Precondition**是trigger action的前置條件
        * 實際**trigger action**的是triggering event
    * Coverage FSM
        * **Node Coverage**:執行每個state
        * **Edge Coverage**:執行每個transition
        * **Edge-Pair Coverage**:執行每個transition-pair
        * **Data flow**
    * How to derive FSM?
        * 由一些document可以幫助tester更快的建立FSM，e.g. system requirement, transition table, UML model
        1. **Combining** control flow graphs(CFGs)
            ![CFGs for example](https://imgur.com/Ud9rRZP.png)
            * **不是準確描述系統的FSM**，因為CFG只是把流程connect在一起，但沒辦法表現出caller和callee之間的關係
            * 以CFG而言，可以建立如上圖(分開的狀態)，但是第6, 8, 10都可能呼叫change time method，而return時又要返回6, 8, 10的哪一個呢?相關的資訊並不會被記錄在node中
        2. Using the **software structures**
            ![Software Structure for example](https://imgur.com/VQDcv1z.png)
            * 以method當作一個node
        3. Modeling **state variables**
            * 只要有state variable就有機會可以實踐這個方法
            * ![state variable](https://imgur.com/p5b9jWI.png)
            * ![relevent state variable](https://imgur.com/4bhzoAn.png)
            * 因為watch, stopwatch和alarm這三者互相獨立，所以只需要9種狀態
            * ![example of watch](https://imgur.com/N7KwvGK.png)
        5. Using implicit or explicit **specifications**
            * Explicit requirement
            * Using intuition and experience when no explicit requirement
    * Summary-Tradeoffs in Applying Graph Coverage Criteria to FSMs
        * **Pros**
            * 在實作**之前**就可以先設計testing
            * 分析FSMs比分析source code容易很多
        * **Cons**
            * 一些實施決策沒有辦法在FSM中建構出模型->複雜的program(有太多的狀態)
            * 由於推導FSM時會有一些主觀性質，造成結果存在一些差異
            * 測試必須“映射”到程序的實際輸入，出現在FSM中的名稱可能與程序中的名稱不同

# 2.6 Graph Coverage for Use Cases
* UML Use Cases: 就是各式的結構、圖形、邏輯等整合在一起，讓學界及業界在開發同一份project可以更無縫的整合，支援的IDE有Visual Studio->由diagram產生C#、Java等template或是反過來也可以
* Pros: 節省開發時間(原本是畫出diagram後還要依照requirement再寫出程式->2倍時間)，且如果implement時發現有東西要修改，大部分的programmer都會直接修改code而忽略修改diagram，到最後design和implementation做的事情就會越來越遠，不利於公司的QA
* Graph in UML - supporting many dagram styles
    * Structure diagram
        * component diagram
        * class diagram
    * Behavior diagram
        * activity diagrams
        * use case diagrams
        * statecharts
    * Interaction diagram
        * sequences diagram
        * communication diagram
* Use Case: 系統操作的各種情境，或者說使用案例
* Use Case Example
    ![Use Case Example](https://i.imgur.com/VrJ7QJp.png)
    * 人的symbol代表一個role
    * 橢圓形的內容就是Use Cases
* Elaboration: 利用附屬文件產生更詳細的model
    * **Use Case Name**
    * **Summary**: 對於project整體的總結
    * **Actor**
    * **Precondition**
    * **Description**: 正常操作的細節
    * **Alternatives**: 步驟出現例外情況(catch & exception)
    * **Postcondition**: 當use case結束之後，應該有的狀態是甚麼
* Use Case to Activity Diagrams: activity diagram約等於CFG，就是從user requirement中操作的step
    ![Activity Graph](https://imgur.com/Za78cae.png)
* Covering Activity Graphs
    * **Node Coverage**
    * **Edge Coverage**
    * **Scenario Testing**
* Summary of Use Case Testing
    * Use cases定義在**requirement** level
    * Very **high level**
    * UML **Activity Diagrams**在圖中encode use cases
        * 圖通常具有相當**簡單的結構**
    * **Requirement-based** testing可以使用graph coverage
        * 直接用手做
        * Specified path coverage對這些圖有意義