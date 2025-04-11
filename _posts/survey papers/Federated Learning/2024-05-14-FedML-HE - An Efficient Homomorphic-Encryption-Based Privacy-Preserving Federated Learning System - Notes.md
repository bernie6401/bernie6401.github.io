---
title: FedML-HE - An Efficient Homomorphic-Encryption-Based Privacy-Preserving Federated Learning System - Notes
tags: [Meeting Paper, NTU]

category: "Survey Papers/Federated Learning"
---

# FedML-HE - An Efficient Homomorphic-Encryption-Based Privacy-Preserving Federated Learning System - Notes
###### tags: `Meeting Paper` `NTU`
:::info
Jin, W., Yao, Y., Han, S., Joe-Wong, C., Ravi, S., Avestimehr, S., & He, C. (2023). FedML-HE: An Efficient Homomorphic-Encryption-Based Privacy-Preserving Federated Learning System. arXiv preprint arXiv:2303.10837.
:::
[TOC]

## Background
### [聯邦學習：攻擊方式](https://ithelp.ithome.com.tw/articles/10302263?sc=iThelpR)
:::spoiler 
> 成員推理攻擊
> 攻擊者試圖確定某些資料是否是訓練的一部分與模型反轉攻擊一樣，攻擊者利用返回的分類分數來創建多個這些 影子 模型，模型與受攻擊的原始模型具有相似的分類邊界。
給定一個 黑盒 機器學習模型和一個資料記錄，確定該記錄是否用作模型的訓練資料集的一部分，被證明是可能的，具有極高的準確性。
因此，僅對在給定輸入上返回模型輸出的黑盒 API 進行簡單的查詢訪問，就可能洩露有關模型訓練所依據的各個資料記錄的大量訊息。
推理攻擊的準確性隨著類別數量的增加而增加。
:::
---
### [What is Multi Party Computation (MPC)?](https://www.eettaiwan.com/20220609nt21-multi-party-computation/)
:::spoiler 
> 一方面，這突破了我們對溝通、合作與娛樂方式的想像，但另一方面，這也使得我們更容易受到資料誤用與竊取的侵害，尤其當這些資料與內部安全金鑰全都列為集中式管理。於是朝向安全多方運算(multi-party computation，MPC)技術發展。
>
>MPC技術是加密技術的次分支。利用這項技術，不同機構或是同一機構內部的不同部門在使用各自的私密資料來共同進行運算時，可以避免向彼此或第三方揭露這些資料，就能取得運算結果。
>
>imec設於比利時魯汶大學的「電腦安全與產業密碼學(Computer Security and Industrial Cryptography，COSIC)研究團隊」將於本文探討MPC技術可行或不可行的觀點及在哪些應用上發揮附加價值，並分析這項密碼學奇蹟為何還在尋找商用的甜蜜點。

有關MPC更詳細的說明請參閱[Secure multi-party computation (MPC) 介绍](https://zhuanlan.zhihu.com/p/100648606)
:::

---
### [What is Differential Privacy? - Apple 怎麼安全的收集我們的隱私？Differential Privacy 的簡介與應用](https://zhuanlan.zhihu.com/p/371101755)
:::spoiler 
> ### Differential Privacy
>
>Differential Privacy (DP) 是一種隱私保護 (Privacy-Preserving) 的演算法，可以在收集群體資料的同時能夠保護單體用戶的 Data。從應用領域來說，DP 不能保護用戶的數據不被看見，但是 DP 能做到的是保護「數據與單個用戶的關聯」。
>
>DP的概念很簡單，就是加入隨機性。如果匿名數據裡面包含的數據是經過隨機處理的，那就很難通過其他線索來反推回個人數據。以 Netflix Prize Data 的例子中，DP 的隨機性可以加入在用戶評分或是評分日期中，甚至可以稍微擾亂電影 ID。只要用戶評價的數據有稍微的隨機性，就很難透過 IMDB 之類的第三方數據反推回用戶 ID。
>
>加入隨機性的程度會影響隱私保護的程度。通常隨機性參數會用符號 ε (epsilon) 來表示，因此也被稱為 ε- Differential Privacy。在 DP 中，「隱私保護」與「數據可用性」往往是一個 Trade-off，因此選擇適當的 ε 也是至關重要。
> ### Differential Privacy 的適用時機
>
>Differential Privacy 是一種應用層面很廣的隱私保護方法。在實務中，DP 幾乎是另用領域最廣的隱私保護算法，因為他的方法足夠簡單，在各種任務中都可以順利應用，例如：推薦算法、趨勢預測、用戶分群等等。
>
>但是 DP 對於數據無可避免的傷害也限制了他的可用性，因此對於一些對於數據要求較高的機器學習算法，例如機器視覺，就不太能夠直接使用。
:::
---
### [What is CKKS?](https://blog.csdn.net/weixin_43466027/article/details/118792866)
> CKKS是2017年提出的同態加密方案。它支持浮點向量在密文空間的加減乘運算並保持同態，但是只支持有限次乘法的運算。

詳細的算法可以參考原文章

---
### [什麼是 DevOps？](https://ithelp.ithome.com.tw/articles/10184557)
:::spoiler 
> DevOps 簡而言之，就是 Development + Operations ，也就是開發與維運。但大部分的文章都會說是「開發」「測試」「維運」三者的結合。如同下面這張圖想表示的意義一樣，當三者有了交集，即是 DevOps
> ![](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Devops.svg/512px-Devops.svg.png)
> #### DevOps 想要達成的目標為何？
>
>從 Patrick Debois 發現的問題與參考葉大一句話囊括 DevOps 的目標一文，可以了解，最大的目標即為速度。「天下武功，唯快不破」，從發現需求到產品上線的時間越短，能得到的回饋與市場也就越大；但快還不夠，還要好，也就是要有品質！如果只有快，而沒有品質，只是更快把 bug 上線，並破壞企業名聲而已。如何兼顧速度與品質，即為 DevOps 的主要目標。
DevOps 到底在做什麼？
>
>為何會出現 DevOps ，相信已經有個感覺了。那它究竟在做些什麼事呢？
>
>有文章會提到用 CALMS 的角度來說明 DevOps 的要領，這是下列五個英文單字的縮寫：
> * Culture
> * Automation
> * Lean
> * Measurement
> * Sharing
> 
> 這是了解 DevOps 概念的好方向之一。
:::

---
### [什麼是MLOps？-30 Days of MLOps](https://ithelp.ithome.com.tw/articles/10238335)
:::spoiler 
> 用最短的一句話來解釋它的話，MLOps 就是 Machine Learning 的 DevOps
> 在 Machine Learning 團隊中，除了資料科學家、資料工程師、DevOps 工程師作為固定班底外，協作單位還有產品經理、後端工程師等等。我們要讓所有人可以彼此良好的協作，這需要依賴更好的維運架構。除了最直覺想到的 Model 部署外，常見的挑戰還有例如：訓練 Model、測試與分析 Model、資料的預處理等等。
> ![](https://github.com/alincode/30-days-of-mlops/raw/master/assets/mlops-collenges.png)
:::
## Homomorphic Encryption Libraries
* [Palisade](https://zhigang-chen.github.io/Palisade/)
* [SEAL - Microsoft](https://hackernoon.com/zh/%E5%BE%AE%E8%BD%AF%E5%8D%B0%E7%AB%A0%E5%92%8C%E5%90%8C%E6%80%81%E5%8A%A0%E5%AF%86%E7%9A%84%E9%BB%8E%E6%98%8E)
### [微軟開源同態加密函式庫SEAL](https://www.ithome.com.tw/news/127457)
:::spoiler 
> 微軟宣布開源簡單加密演算法函式庫（Microsoft Simple Encrypted Arithmetic Library，Microsoft SEAL），這是一個由微軟加密研究小組研發，容易使用的同態加密（Homomorphic Encryption）函式庫，現在於GitHub以MIT授權許可開源。
>
>越來越多資料被搬上雲端，微軟提到，他們遭遇到了便利性與隱私性的權衡問題，在考量投資利益最大化的情況下，需要盡可能的改善服務效能，或是讓傳輸更加有效率。作為交換，微軟與服務供應商共享個人資訊，不過，在傳統的加密架構下，無法在加密資料上進行任何計算，也就是說，無法在未將資料解密的情況下，供第三方進行資料操作。
>
>其中一種解決方法，便是把加密資料儲存在雲端，當需要的時候下載以執行有用的操作，微軟提到，這樣的方法在實務上邏輯不通，而另一種方法則是提供服務供應商解密金鑰，但這又暴露了隱私風險。
>
>同態加密則能解決這個問題，同態加密允許在加密資料上進行額外的處理，包括檢索或是比較等操作，整個過程不需要對資料進行解密，就能獲得正確的結果，而這在根本上解決了將資料及操作委託給第三方時，遭遇的保密問題。同態加密函式庫Microsoft SEAL的出現，允許微軟在不暴露個人訊息的狀況下，提供第三方應用雲端操作。

---
## Model Compression
[Low Rank Decomposition 低秩矩阵分解 - Vid.](https://www.bilibili.com/video/BV15E411A7hB/?share_source=copy_web&vd_source=31529c2d248aba29c9cc1e3cbd720cb6)
[Lec06 深度學習的模型壓縮與加速 Low Rank Approximation (6/9)](https://youtu.be/cbFkMGQqAOA)
簡單來說就是把原本的model做拆解，變成比較小的rank，這樣的好處是運算的速度會比較快，但缺點是運算的error會增加，畢竟是拆解，也不見得能夠一模一樣
![](https://hackmd.io/_uploads/Syen9UjOSh.png)

從以下實驗結果來說，左側有提到幾倍的運算效能的提升，但右邊也顯示了這樣會造成error的增加
![](https://hackmd.io/_uploads/HyKxwjdH3.png)

---
## Implementation Note
[Federated Learning on AWS with FedML: Health analytics without sharing sensitive data – Part 1](https://aws.amazon.com/tw/blogs/machine-learning/part-1-federated-learning-on-aws-with-fedml-health-analytics-without-sharing-sensitive-data/)

---
### [Cross-Silo VS. Cross-Device in FL](https://worktile.com/kb/p/48518)
:::spoiler 
> #### 模式不同
> * Cross-device聯邦學習：多設備聯邦的模式。
> * Cross-Silo聯邦學習：與跨設備聯合學習的特征相反，Cross-Silo 聯邦學習在總體設計的某些方面非常靈活。許多組織如果只是想共享訓練模型，而不想分享數據時，cross-silo設置是非常好的選擇。Cross-Silo 聯邦學習的設置主要有以下幾個要點：數據分割、激勵機制、差異隱私、張量因子分解。
> #### 面對的客戶端不同
> * Cross-device聯邦學習：Cross-device FL針對的則是便攜式電子設備、穿戴式電子設備等，統稱為物聯設備（Internet of Things, IoT devices）。
> * Cross-Silo聯邦學習：Cross-silo FL面對的客戶端是企業級別、機構單位級別的。
> #### 客戶端狀態不同
> * Cross-device聯邦學習：無狀態，每個客戶可以僅會參與一次任務，因此通常假定在每輪計算中都有一個從未見過的客戶的新樣本。
> * Cross-Silo聯邦學習：有狀態，每個客戶端都可以參與計算的每一輪，並不斷攜帶狀態。
> #### 可定位性不同
> * Cross-device聯邦學習：沒有獨立編號，無法直接為客戶建立索引。
> * Cross-Silo聯邦學習：有獨立編號，每個客戶端都有一個標識或名稱，該標識或名稱允許系統專門訪問。
> #### ...
:::

---
### [什麼是 Amazon EC2？](https://docs.aws.amazon.com/zh_tw/AWSEC2/latest/UserGuide/concepts.html)
:::spoiler
> Amazon Elastic Compute Cloud (Amazon EC2) 在 Amazon Web Services (AWS) Cloud 中提供可擴展的運算容量。使用 Amazon EC2 可減少前期所需的硬體投資，讓您更快速開發並部署應用程式。您可使用 Amazon EC2 按需要啟動任意數量的虛擬伺服器，設定安全性和聯網功能以及管理儲存。使用 Amazon EC2 可擴展與縮減規模，以處理需求或熱門峰值的變更，從而降低您預測流量的需求。
> ### Amazon EC2 提供以下功能：
> * 虛擬運算環境，亦即執行個體
> * 供執行個體使用的預先設定範本，亦即 Amazon Machine Images (AMI)，在其中封裝伺服器所需的元件 (包括作業系統和其他軟體)
> * 執行個體 CPU、記憶體、儲存和聯網功能的各種組態，亦即執行個體類型
> * 使用金鑰對來保護執行個體的登入資訊 (AWS 會存放公有金鑰，而您則於安全位置存放私有金鑰)
> * ...
:::

---
### [MQTT教學（一）：認識MQTT](https://swf.com.tw/?p=1002)
:::spoiler 
> #### 比較HTTP和MQTT通訊協定
>
> MQTT和HTTP的底層都是TCP/IP，也就是物聯網裝置可以沿用既有的網路架構和設備，只是在網路上流通的「訊息格式」以及應用程式的處理機制不同。
> ![](https://swf.com.tw/images/books/IoT/MQTT/mqtt_tcp_ip.png)
> #### MQTT訊息格式
>
> 採用MQTT發布溫度的訊息格式類似這樣：
> ![](https://swf.com.tw/images/books/IoT/MQTT/mqtt_messge.png)
> 不同於HTTP的標頭採用文字描述，MQTT的標頭採用數字編碼，整個長度只佔2位元組，等同兩個字元，後面跟著訊息的主題（topic）和內容（payload），實際格式如下：
> ![](https://swf.com.tw/images/books/IoT/MQTT/mqtt_message_format.png)
:::

---
### [What is Amazon S3?](https://docs.aws.amazon.com/zh_tw/iot/latest/developerguide/s3-rule-action.html)
> S3 (s3) 動作會從 MQTT 訊息將資料寫入 Amazon Simple Storage Service (Amazon S3) 儲存貯體。