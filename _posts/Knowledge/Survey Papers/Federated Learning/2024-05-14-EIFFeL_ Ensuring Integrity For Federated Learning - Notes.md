---
title: 'EIFFeL: Ensuring Integrity For Federated Learning - Notes'
tags: [Meeting Paper, NTU]

category: "Knowledge｜Survey Papers｜Federated Learning"
date: 2024-05-14
---

# EIFFeL: Ensuring Integrity For Federated Learning - Notes
<!-- more -->
###### tags: `Meeting Paper` `NTU`
:::info
Roy Chowdhury, A., Guo, C., Jha, S., & van der Maaten, L. (2022, November). Eiffel: Ensuring integrity for federated learning. In Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security (pp. 2535-2549).
:::

## Background
* [聯邦學習的簡單介紹](https://medium.com/%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92%E7%9F%A5%E8%AD%98%E6%AD%B7%E7%A8%8B/%E8%81%AF%E9%82%A6%E5%AD%B8%E7%BF%92%E7%9A%84%E7%B0%A1%E5%96%AE%E4%BB%8B%E7%B4%B9-776924277d13)
    > 聯邦學習的流程大致上可以分成4步驟：
    > * 確定架構(拓樸) Formulate topology
    > * 梯度計算 Gradient compute
    > * 資訊交換 Information exchange
    > * 模型聚合 model aggregation

* [What is Secure Aggregation?](https://zhuanlan.zhihu.com/p/83786131)

* [What is Byzantine attacks?](https://aisigsjtu.github.io/projects/fl-attack-defense/)
    > 目前針對聯邦學習的拜占庭攻擊主要分為三種模式。
    > * 數據污染攻擊，是通過在客戶端本地數據集中加入污染過的圖片使得客戶端上傳的模型準確度很差，進而影響全局模型。常見的數據污染攻擊包括標簽反轉攻擊（Label-flipping Attack）、基於反向梯度優化的攻擊（Back-gradient optimization based attack）等等。相比於其他方式，數據污染攻擊的攻擊強度比較弱、攻擊精度比較差，但是比較容易進行。
    > 
    > * 模型污染攻擊，是在模型的訓練過程中以及傳輸過程中進行修改，不涉及對本地數據的變更，代表是局部模型污染攻擊（Local Model Poisoning Attack）。模型污染攻擊的攻擊強度很高，並且可以進行更有針對性的攻擊，但是相應的也需要對客戶端更多的控制權。
    > 
    > * 第三種攻擊模式是前兩種攻擊的融合，比如目標模型污染（Targeted Model Poisoning）和隱式模型污染（Stealthy Model Poisoning）。第三種模式不但會修改被控制的客戶端的本地數據，而且也會對模型訓練過程進行影響。相比於前兩種攻擊方式，第三種攻擊方式不但擁有較好的隱秘性而且還擁有很強的精確性。


    > * 如何防禦：
    > 1. 傳統的比較流行的方式有Chen等人提出的GeoMed算法，這是一種基於幾何中值的聚合規則。
    > 2. Blanchard等人則是在聚合過程中加入了Krum函數，通過比較權重之間的距離來選擇威脅度最小的權重進行更新。
    > 3. 而Yin等人則提出了Trimmed Mean算法，通過去掉最大最小值之後進行權重的平均來更新全局的模型。
    > 4. 綜合考慮多項指標的方法，比如向服務器端引入小的根數據集，並用根數據集訓練小模型來以此為標準進行惡意客戶端篩選的FLTrust。
    > 5. 引入其他機器學習思想的方法，比如Justinian’s GAAvernor利用了強化學習，在服務器端訓練一個魯棒性很強的輔助模型來幫助服務器進行選擇。

* What is secret-shared non-interactive proofs and example - from ChatGPT:
    > Secret-shared non-interactive proofs are a type of cryptographic protocol that allows multiple parties to jointly prove the correctness of a computation, without revealing any private information about their inputs.
    >
    >In a secret-shared non-interactive proof, the computation is divided into multiple parts, and each party holds a share of the inputs and outputs of the computation. The parties can then jointly prove the correctness of the computation by exchanging messages with each other, without revealing their shares of the inputs and outputs.
    >
    >This type of protocol is particularly useful in scenarios where multiple parties need to collaborate on a computation while preserving the privacy of their inputs. For example, secret-shared non-interactive proofs can be used in multi-party computation to allow multiple parties to jointly compute a function on their private inputs, without revealing those inputs to each other.
    >
    >Overall, secret-shared non-interactive proofs are an important tool in modern cryptography for enabling secure and private computation in collaborative settings.

    ---
    Example:
    >Suppose that Alice, Bob, and Charlie each have a secret number, x, y, and z respectively, and they want to compute the sum of their three numbers without revealing their individual inputs to each other.
    >
    >To achieve this, they can use a secret-sharing scheme such as Shamir's secret sharing to split each of their numbers into multiple shares, such that no single share reveals any information about the original number. Each party then distributes their shares to the other two parties.
    >
    >Next, they can use a secret-shared non-interactive proof protocol to jointly prove that they have correctly computed the sum of their shared numbers, without revealing their individual shares to each other. For example, they can use a zero-knowledge proof protocol to prove that the sum of the shares they hold is equal to the sum of their original numbers.
    >
    >Once the proof is complete, they can use the shared values to compute the sum of their three secret numbers without revealing any information about their individual inputs.
    >
    >Overall, this example demonstrates how secret-shared non-interactive proofs can be used to enable secure and private multi-party computation.

    :::spoiler Chinese Version
    秘密共享的非交互式證明是一種加密協議，它允許多方共同證明一個計算的正確性，而不透露任何關於他們輸入的私人信息。

    在秘密共享的非交互式證明中，計算被分為多個部分，每一方都持有計算的輸入和輸出的份額。然後，各方可以通過互相交換消息來共同證明計算的正確性，而不透露他們在輸入和輸出中的份額。

    這種類型的協議在多方需要合作進行計算的情況下特別有用，同時保留他們輸入的隱私。例如，秘密共享的非交互式證明可以在多方計算中使用，以允許多方在他們的私人輸入上聯合計算一個函數，而不把這些輸入透露給對方。

    總的來說，秘密共享的非交互式證明是現代密碼學的一個重要工具，可以在協作環境中實現安全和隱私的計算。


    假設愛麗絲、鮑勃和查理各自有一個秘密數字，分別是x、y和z，他們想計算他們三個數字的總和而不向對方透露他們各自的輸入。

    為了實現這一點，他們可以使用秘密共享方案，如Shamir的秘密共享，將他們的每個數字分成多個份額，這樣，任何一個份額都不會泄露關於原始數字的任何信息。然後，每一方將他們的份額分配給另外兩方。

    接下來，他們可以使用秘密共享的非交互式證明協議來共同證明他們已經正確地計算了他們共享的數字之和，而不向對方透露他們各自的份額。例如，他們可以使用一個零知識證明協議來證明他們持有的份額之和等於他們的原始數字之和。

    一旦證明完成，他們就可以使用共享值來計算他們三個秘密數字的總和，而不透露任何關於他們個人輸入的信息。

    總的來說，這個例子展示了秘密共享的非交互式證明如何被用來實現安全和隱私的多方計算。
    :::
    
* [What is Probabilistic Polynomial Time?](https://blog.csdn.net/cw397265362/article/details/121385234)
    > A probabilistic polynomial-time (PPT) algorithm A is an algorithm that runs in polynomial time but also has access to some oracle which provides true random bits. So if we input x into A, instead of getting an output y=A(x) that is a deterministic value, we get a random variable Y which has a certain probability of being a set of different values.
    > 概率多項式時間（PPT）算法A是一種在多項式時間內運行的算法，但也可以訪問一些提供真正隨機比特的預言機(不太懂)。因此，如果我們把x輸入A，不是得到一個確定性的輸出值y=A（x），我們得到一個隨機變量Y，它有一定的概率是一組不同的值


* [神奇的零知识证明！既能保守秘密，又让别人信你！](https://youtu.be/FuKEpOhiVPg)
    > 要達到零知識證明需要三個條件：
    > 1. 完備性(Completeness)：真的假不了；假如Prover掌握某種訊息，則Prover可以很輕易的回答Verifier所提出的問題，且Verifier也可以很輕鬆的驗證答案的正確性
    > 2. 合理性/正確性(Soundness)：假的真不了；假如Prover沒有掌握某種訊息，則Prover有極高的機率會回答錯誤
    > 3. 零知識(Zero knowledge)：對答的過程中，不會透漏任何有關關鍵訊息的資訊

* [【隐私计算笔谈】MPC系列专题（五）：Beaver三元组和BMR协议](https://blog.csdn.net/Matrix_element/article/details/117788407)