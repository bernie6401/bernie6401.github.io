---
title: 'The State of Ethereum Smart Contracts Security: Vulnerabilities, Countermeasures, and Tool Support - Notes'
tags: [Meeting Paper, NTU]

category: "Survey Papers/Digital Currency"
---

# The State of Ethereum Smart Contracts Security: Vulnerabilities, Countermeasures, and Tool Support - Notes
<!-- more -->
###### tags: `Meeting Paper` `NTU` `Seminar`
:::info
Zhou, H., Milani Fard, A., & Makanju, A. (2022). The state of ethereum smart contracts security: Vulnerabilities, countermeasures, and tool support. Journal of Cybersecurity and Privacy, 2(2), 358-378.
:::

## Background
:::spoiler [以太幣(Ether) VS 以太坊(Ethereum)](https://rich01.com/what-is-ether-ethereum/)
>以太坊是一個區塊鏈平台，而以太幣是裡面所使用的貨幣，智能合約的運算費用、區塊鏈上的交易手續費、礦工挖礦的獎勵等，都會用以太幣支付。
>
> 以太坊目的是打造一個「去中心化的世界電腦」，執行的方式是透過區塊鏈技術，實現去中心化智能合約平台，以太坊和比特幣一樣具有可挖礦的公鏈系統，但多了智能合約、Dapp的技術。
:::
:::spoiler [What is Smart Contract?](https://rich01.com/what-is-smart-contract/)
> 智能合約是一種將雙方的協議條款，並用代碼形式在區塊鏈上運行，儲存在一個公共資料庫中，不能被更改。
>
> 智能合約中發生的交易是由區塊鏈處理的，這意味著它們可以在沒有第三者的情況下自動執行，只有當協議中的條件得到滿足時，交易才會發生，是完全去中心化的交易。

> ## 智能合約 VS 傳統合約
> ![](https://rich01.com/wp-content/uploads/20210917180100_80.jpg)
> ### 傳統合約
> 雙方合作簽約後，雙方或者多方協議，做或不做某事來換取某些東西，而合約中的任何一方必須信任彼此並履行義務。同時還必須有個第三方的執法機構介入，若是有一方違反條款，就需要這個執法機構進行判決。
> ### 智能合約
> 雙方合作線上簽署合約，合約為一個運行在區塊鏈的代碼，儲存在一個公共資料庫中，不能被更改。雙方或者多方協議，做或不做某事來換取某些東西，但不需要信任彼此，因為合約內容會完全自動強制執行，公開透明不會被更改。
> 
> ### 舉例來說
> 如果小明要買大明的房子，簽訂的是智能合約，合約運行在以太坊區塊鏈，合約內容為：當小明向大明支付300個以太幣時，小明將獲得房子的所有權。
>
> 一旦這個智能合約簽訂好就不能被改變，這意味著小明可以放心支付300個以太幣來買大明的房子，而不用擔心大明反悔。如果是使用傳統合約，小明買房子可能要支付第三方公司的大量費用，例如銀行、律師和房屋經紀人、佣金…等等，也需要花費許多的時間。但使用了智能合約，不僅完全省略了第三方公司的介入，也可以縮短整個合約進行的時間。
:::

:::spoiler [What is Solidity?](https://ithelp.ithome.com.tw/articles/10202884)
> Solidity 是一種合約式導向的程式語言，用來撰寫智能合約，它受到 C++、Python 和 `Javascript` 語言影響，語法設計參考了 ECMAScript，所以對於寫過 `Javascript` 的人，相對好上手。
> 
>Solidity 是靜態型語言，編譯後可以在 `EVM` 上執行。撰寫以太坊的智能合約，除了可以用 Solidity 語言，還有 `Vyper` 語言可以選擇。
> 
> `EVM` (`Ethereum` Virtual Machine)：中文翻譯為「以太坊虛擬機」，是智能合約的運行環境。
:::
:::spoiler [What is Merkle Patricia Tree](/@pohanlu/Merkle_Patricia_Tree)
> * 是一種經過改良的、融合了Merkle tree (hash tree)和Radix tree 的優點的數據結構
> 
> * 可以理解為把帳本分割成無數個小的資料塊，每個資料塊像是一棵樹中的無數葉片，而我們把每兩個相鄰的葉片合併成一個字串，並算出該字串的 Hash 值。經過無數次後，會得到一個包含了所有區塊資料的 Hash 值，稱為「Merkle Root」
:::
:::spoiler [【區塊鏈入門】到底什麼是Gas、Gas Price、Gas Limit？](https://guide.blocto.app/article/gas-gas-price-gas-limit)
> 以太坊網路，也被稱為 Ethereum 區塊鏈。Ether（ETH）是該網路的燃料。當您發送代幣時，進行合約發送 ETH 或在區塊鏈上執行其他任何操作時，您必須為該計算付費，交易手續費以 Gas 計算，並以 Ether 支付。
>
>Ethereum 區塊鏈內進行任何交易、執行智能合約、啟動 DApps 和支付數據存儲的手續費都被礦工收取。礦工對交易進行確認並確定哪些交易能進入新區塊。無論您的交易是成功還是失敗，您都需計算付費。即使失敗，礦工也必須驗證並執行您的交易（驗算），因此您必須支付驗算費用，就像成功支付交易一樣。
:::
:::spoiler [What is Dapp](https://rich01.com/what-is-ether-ethereum/)
> Dapp (英文：Decentralised Application)是一個去中心化的應用程式，具有公開、不可竄改的特性。
>
>舉個例子：
像是我們在手機APP上玩小遊戲，這些遊戲數據都會傳到軟體公司的後台伺服器，但是要怎麼知道軟體公司有沒有偷改伺服器資料呢？
>
>所以就有人把遊戲寫成Dapp形式，公開遊戲程式並放到區塊鏈上，這樣沒有任何人可以更改程式內容，就連發佈者也不行。
>
>這就是一種去中心化應用程式的概念(具有透明公開、不可竄改、絕對忠實執行程式碼的特性)。
:::

:::spoiler [NIST & CFS](https://docs.aws.amazon.com/zh_tw/audit-manager/latest/userguide/NIST-Cybersecurity-Framework-v1-1.html)
> # 什麼是 NIST 網路安全架構？
>
>美國國家標準與技術研究所（NIST）
>
>成立於 1901 年，現在是美國商務部的一員。NIST 是美國最古老的物理科學實驗室之一。美國國會成立了該機構，以改善當時的二流測量基礎設施。該基礎設施是美國工業競爭力的一大挑戰，已落後於英國和德國等其他經濟大國。
>
>美國取決於關鍵基礎設施的可靠運作。網絡安全威脅利用關鍵基礎設施系統日益複雜性和互連性。他們使美國的安全，經濟和公共安全和健康處於危險之中。與財務和聲譽風險類似，網絡安全風險會影響公司的利潤。它可以提高成本並影響收入。它可能會損害組織的創新能力，以及獲得和維護客戶的能力。最終，網絡安全可以擴大組織的整體風險管理。
>
>NIST 網路安全架構 (CSF) 受到全球各國政府和產業的支援，作為任何組織使用的建議基準，無論產業或規模如何。NIST 網路安全架構包含三個主要元件：架構核心、設定檔和實作層。框架核心包含所需的網絡安全活動和成果，分為 23 個類別，涵蓋了組織的廣泛網絡安全目標。配置文件包含組織對其組織需求和目標，風險偏好以及使用框架核心所需結果的資源的獨特一致性。實施層描述了組織的網絡安全風險管理實踐表現框架核心中定義的特徵的程度。
:::
:::spoiler [DAO遭駭事件](https://www.ithome.com.tw/news/107405)
> ## Attack Method
> 在攻擊前一周，駭客先提出一項研究專案，向The DAO平臺（母DAO專案）申請研究經費，專案通過後，因此分出一個DAO子專案，並在一周後執行智能合約分割功能splitDAO來建立新專案。
>
>接著母DAO專案會透過Token建立程序，先撥款（以太幣）給子DAO專案，之後才進行扣款動作，來刪減母DAO帳目的以太幣數目。不過，當母DAO執行withdrawRewardFor程式，要撥款給子DAO時，駭客透過自訂智能合約的功能，再次呼叫splitDAO功能，趕在扣款指令還未進行之前，再次執行專案建立功能進行再次撥款，因扣款完成前，用戶以太幣餘額仍是正值，在母DAO來不及更新平衡帳目前，這項新建專案和撥款的動作，可以不斷地重複執行。
>
>高靖鈞說，透過遞迴的攻擊，駭客讓母DAO不斷撥款，最後一共盜領了約370萬個以太幣，以當時以太幣市價每個約20美元來計算，遭竊了價值約7,200萬美元的以太幣。
:::
:::spoiler [What is Common Weakness Enumeration, CWE](https://ithelp.ithome.com.tw/articles/10203970)
> CWE這個計畫中維護了一個軟體弱點的列表，而這個計劃的主要目的是希望能夠建構一個描述軟體存在於架構、設計或程式碼中安全威脅的通用語言，而且能夠成為一個軟體安全工具在修補弱點時能參照的標準，更重要的是，能夠透過這樣的列表，將每個弱點的特徵、緩解方式及預防方式記錄下來，讓所有人能夠參考應用。
> [CWE Website Link](https://cwe.mitre.org/top25/)
:::
:::spoiler [開發智能合約 - ABI](https://ithelp.ithome.com.tw/articles/10201750)
>  ABI (Application Binary Interface)
>
>   ABI 裡記載了智能合約提供哪些函式，以及應該要傳入什麼樣的參數。
>    當你要開發 DApp 時，需要兩個值，才能跟智能合約溝通，一個是合約位址，另一個就是一個是 ABI 了。
:::


## Content Note
:::spoiler [Function Signature & Function Selector](https://ithelp.ithome.com.tw/articles/10287327)
> Function 的完整字串實際上也就是所謂的 Function Signature，而哈希過後得到的 ABI Byte String 便是 Function Selector。
> * 當我們要和「不需要」任何參數的 "Getter" Function 互動時，可以取函式簽章進行 keccak256 hash 後的前四個 bytes
        function myUint()
        bytes4(keccak256("myUint()"));
> * 當我們要和「需要」參數的 "Getter" Function 互動時，則需要把參數型態也包入進行 hash 再取前四個 bytes
        function someFunction(uint _myUint1, address _someAddr)
        bytes4(keccak256("someFunction(uint256,address)"))

![](https://chineself.com/wp-content/uploads/2022/09/jugelizi.png)
```solidity!
contract MyContract {
    function myFunction(uint256 arg1, string memory arg2) public returns (bool) {
        // function implementation
    }
}

// Call myFunction with function signature
function callMyFunction(address contractAddress) public {
    bytes4 functionSelector = bytes4(keccak256(bytes("myFunction(uint256,string)")));
    bool success = contractAddress.call(functionSelector, 123, "hello world");
    require(success, "Function call failed.");
}

```
正常來說應該是要像這樣，在call function之前，利用hash function把function signature做hash，變成function selector之後才能呼叫和傳參數，所以如果沒有做這個動作的話，就會觸發fallback function，這樣就有Re-Entrancy的風險

目的：
> @楊冠彥: 因為在智慧合約部分我們最終要轉換為bytecode給電腦讀，那function signature就是你寫的一個function，之後要轉換為function selector，顧名思義要對該function簽章
:::

:::spoiler Delegatecall VS Call and its vulnerability
[Delegatecall VS Call](https://youtu.be/wJiV6OWoOpQ)
其實就是call function後的結果會被保留的地方不同而已，比方說合約DelegateCall要"**Call**"合約TestDelegateCall，則運算的數值(`num` & `sender`)會被保留在合約TestDelegateCall，但是如果合約DelegateCall要"**delegateCall**"合約TestDelegateCall，則運算的數值(`num` & `sender`)會被保留在合約DelegateCall
```solidity!
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TestDelegateCall
{
    uint public num;
    address public sender;
    
    function setVars(uint _num) public
    {
        num = _num * 2;
        sender = msg.sender;
    }
}

contract DelegateCall
{
    uint public num;
    address public sender;
    
    function setVars(address _contract, uint _num) public
    {
        //(bool success, ) = _contract.delegatecall(abi.encodeWithSelector(TestDelegateCall.setVars.selector, _num));
        
        (bool success, ) = _contract.call(abi.encodeWithSelector(TestDelegateCall.setVars.selector, _num));
        require(success, "Fail to execute delegatecall")
    }
}
```
[Delegatecall Vulnerability](https://youtu.be/aEUZTDOpJ1k)
:::

:::spoiler [3 Address Code](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwijo9isl-P9AhV-S2wGHa7GAVEQFnoECA4QAQ&url=https%3A%2F%2Fwww.geeksforgeeks.org%2Fthree-address-code-compiler%2F&usg=AOvVaw1HPhxt4VwKe2NsWhSJaR7x)
> Three address code is a type of intermediate code which is easy to generate and can be easily converted to machine code. It makes use of at most three addresses and one operator to represent an expression and the value computed at each instruction is stored in temporary variable generated by compiler. The compiler decides the order of operation given by three address code. 
:::

:::spoiler [What is Oyente](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwimx_vQleP9AhUGSGwGHZWzD48QFnoECBUQAw&url=https%3A%2F%2Fwww.alchemy.com%2Fdapps%2Foyente&usg=AOvVaw1jdU-1zG6dzwdkNAD0m9cS)
> Built by Loi Luu and his team at the National University of Singapore, Oyente is a symbolic analysis tool to catch security vulnerabilities in Ethereum contracts and EVM bytecode.
:::

:::spoiler [What is ANTLR](https://blog.miniasp.com/post/2021/07/05/Getting-Started-with-ANTLR-v4-using-NET)
> ANTLR 是一套威力強大的 Parser Generator (解析一份 DSL 語言的程式碼產生器)，可以用來讀取、解析、執行、轉譯一份結構化的文字或二進位檔案。這套工具通常用來打造一個程式語言、工具或框架。
:::

:::spoiler [Taint Analysis & Symbolic Execution](https://ithelp.ithome.com.tw/articles/10293558)
> 污點分析 (taint analysis) 跟符號執行 (symbolic execution)，前者可以知道資料的走向並作分析，後者可以算出如果要走到特定的 function，輸入需要滿足怎樣的條件。當這兩個技術運用在 fuzzing 當中，fuzzer 就能走到條件比較嚴苛的 function，藉此增加程式 coverage，或者就只需要針對輸入中比較有興趣的資料做 mutation。
> * Taint analysis 中文翻譯為污點分析，是一種 data flow tracking 的技巧，通常被用來檢測惡意的資料流向，藉此得知程式當中哪些地方可能會發生問題。
> ---
> 程式當中充斥許多 if-else condition，這些條件判斷使得程式在不同的情況下有不同的處理方式，而每個 condition 都是將各個變數的比較做組合。如果將這些 condition 轉換成數學式子，則會發現有許多共通之處，像是靜態期間變數的值無從得知，就對應到數學當中的未知數；大於、等於與小於的比較在數學中也有相同的行為，因此科學家嘗試用符號表示變數，"模擬"變數的值來執行程式，藉此通過特定路徑，獲得輸出結果，而這樣的處理也被稱作符號執行 (symbolic execution)。
> 概念就是把程式的變數視為符號，並且把走到特定 function 的路徑上所有 if-else 條件組合起來，解出各個符號的值需要在什麼範圍當中，最後產生對應的 input 來滿足這些條件
> * 目前常看見使用到 symbolic execution 的工具有 z3、angr (底層使用 Claripy solver)
:::