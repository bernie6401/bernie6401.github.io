---
title: NTU Software Testing Notes
tags: [NTU_ST, Software Testing, NTU]

category: "Security > Course > NTU ST"
---

# NTU Software Testing Notes
###### tags: `NTU_ST` `Software Testing`
**All content in this presentation is refer to [Pro. Farn Wang Website](http://cc.ee.ntu.edu.tw/~farn/courses/ST/2021.Spring/)**

:::spoiler Click to open TOC
[TOC]
:::

## 6.1 Regression Testing
* Definition
    > The process of re-testing software that has been modified
    > 重複執行既有的全部或部分的相同測試 - by [Esther](https://medium.com/@esther.tsai/%E5%9B%9E%E6%AD%B8%E6%B8%AC%E8%A9%A6-regression-testing-35d69b996481)
* Note that:
    > Most of our testing effort is regression testing
    > Regression tests must be automated
* Type of tools
    * Capture / Replay: Capture values entered into a GUI and replay those values on new versions(抓取輸入到GUI的value並replay到新的版本)
    * Version control: 追踪測試集合、預期結果、測試來源、使用的標準及其過去的有效性(Keeps track of collections of tests, expected results, where the tests came from, the criterion used, and their past effectiveness)
    * Scripting software: 管理以下流程，包含獲取測試輸入、執行軟體、獲取輸出、比較結果和生成測試報告等等(Manages the process of obtaining test inputs, executing the software, obtaining the outputs, comparing the results, and generating test reports
    > Tools are plentiful and cheap
* Managing Tests in a Regression Suite
    * Test suite會不斷累加新的test
    * Test suites通常在晚上執行(固定、一段很短的時間)
* Policies for Updating Test Suites
    * 要保留哪些測試?
        - 確保始終滿足覆蓋標準(**coverage criterions**)
        - Add a new test for every problem report
    * 要刪除那些測試?
        - 無法滿足覆蓋率的測試
        - 從未發現故障的測試（**<font color=#FF0000>Risky!</font>**）
        - 與其他測試發現相同錯誤的測試（**<font color=#FF0000>Risky!</font>**）
    * Reordering strategies
        - If a suite of N tests satisfies a coverage criterion, the tests can often be reordered so that the first **<font color=#00A700>N-x</font>** tests satisfies the criterion – so the remaining tests can be removed
* When a Regression Test Fails
    * Regression tests are evaluated based on whether the test result on the new program `P` is equivalent to the test result on the previous version `P-1`(若不同則代表fail)
    * Fails represent 3 possibilities
        * The software **<font color=#FF0000>has a fault</font>** – Must fix the fix
        * The test values are **<font color=#FF0000>no longer valid</font>** on the new version – Must delete or modify the test(測試端無效可能是待測程式也有可能是new version)
        * The expected output is no longer valid – Must update the test(輸出端無效可能是發現新的問題要測試)
* Evolving Tests Over Time
    * Changes to **external interfaces** can sometimes cause all tests to fail
        * Modern capture / replay tools **will not be fooled by trivial changes** like color, format, and placement
        * Automated scripts can be changed automatically via global changes in an editor or by another script(一些global configuration之類的)
        * 但是小小的改動成本會慢慢累加
* Choosing Which Regression Tests to Run
    * Change Impact Analysis(CIA) - 一個小小的改動會對整體的測試造成多大的影響?
    * Strategy:
        | Strategy | Pros | Cons |
        | -------- | -------- | -------- |
        | <font color=#FF0000>Run all tests</font>| More safety| High cost of time|
        | Based on priority/risk| 可以管控到重大風險的議題| Hard to implement and also need more skills on **evaluating risk**|
        | Based on the function(重要或常用)| The most effective way to improve system reliability on a budget| Hard to implement and also need more skills on evaluating **what is a important function**|
        | <font color=#FF0000>Run revise part</font>| Trivial and small scale| Not comprehensive enough|
        | Selective repeat test (確認正確性和周邊是否受到影響)| Fast and effectively| More skills on analyze the effective part (需要較多技巧在分析上)|
        
<!-- * Rationales for Selecting Tests to Re-Run
    * Inclusive: 當其包含modification revealing test時，選inclusive
    * Precise: 當其省略modification revealing的regression test，選precise
    * Efficient: 當決定省略哪些測試比運行省略的測試更cheap時，選efficient
        * Depends on how much automation is available
    * General: 當適用於大多數實際情況時，選general -->

## 6.2 Integration and Testing
![unintegrate test](https://user-images.githubusercontent.com/88981/52933895-c0d47600-338f-11e9-9034-11e1ad0c42f1.gif)
* Big Bang - Throw all the classes together, compile the whole program, and system test it - **<font color=#FF0000>Risky!</font>**
    * Usually method: start small, with a few classes that have been tested thoroughly (從小地方開始)
        * Add a small number of new classes
        * Test the connections between the new classes and pre-integrated classes
    * Integration testing: testing interfaces between classes
        * Should have already been tested in isolation **<font color=#00A700>(unit testing)</font>**
* Methods, Classes, Packages
    * Integration can be done at the method level, the class level, package level, or at higher levels of abstraction
    * We use the word **<font color=#00A700>component</font>** in a generic sense which is a piece of a program that can **be tested independently**
    * Integration testing is done in several ways
        * Evaluating two specific components
        * Testing integration aspects of the full system
        * Putting the system together “piece by piece”
* Software Scaffolding(鷹架)
是為support integration和testing而創建的extra software components
![process of software scaffolding](https://imgur.com/5V4zxEw.png)
    * Stubs(票根/存根聯): 單純模擬尚未實踐或整合的method，被call的result
    * Drivers: 單純模擬make a call to 正在測試的component(CUT)的方法
* Stubs
    * The first responsibility of a stub is to allow the CUT(Component Under Test) to be compiled and linked without error
    * Approaches:
        1.Return constant values from the stub
        2.Return random values
        3.Return values from a table lookup(回傳查表)
        4.Return values entered by the tester during execution(回傳測試者輸入)
        5.Processing formal specifications of the stubbed method
        * Note that 1 ↦ 5 is more costly / more effective
* Drivers
Many good programmers add drivers to every class as a matter of habit
    * Instantiate objects and carry out simple testing(實例化+簡單測試)
    * Criteria from previous chapters can be implemented in drivers
    * Test drivers can easily be created automatically
    * Values can be hard-coded or read from files
* Class Integration and Test Order (CITO)
    * Which order to integrate was pretty easy:
        * Test the “leaves” of the call tree(測試leaves)
        * Integrate up to the root(整合到root)
        * **Goal is to minimize the number of stubs needed**
    * OO會使其更複雜 - dependencies (call, inheritance, use, aggregation) or circular dependencies : A inherits from B, B uses C, C aggregates A...
    * Which order should we integrate and test?
        * Must "break cycles”
        * Common goal: least stubbing


## Reference
* [回歸測試 regression testing](https://medium.com/@esther.tsai/回歸測試-regression-testing-35d69b996481)
* [一次搞懂單元測試、整合測試、端對端測試之間的差異](https://blog.miniasp.com/post/2019/02/18/Unit-testing-Integration-testing-e2e-testing)