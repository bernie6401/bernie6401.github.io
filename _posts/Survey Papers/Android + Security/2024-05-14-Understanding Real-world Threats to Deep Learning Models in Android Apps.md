---
title: Understanding Real-world Threats to Deep Learning Models in Android Apps
tags: [Meeting Paper, NTU]

category: "Survey Papers｜Android + Security"
---

# Understanding Real-world Threats to Deep Learning Models in Android Apps
<!-- more -->
###### tags: `Meeting Paper` `NTU`
:::info
Deng, Z., Chen, K., Meng, G., Zhang, X., Xu, K., & Cheng, Y. (2022, November). Understanding real-world threats to deep learning models in android apps. In Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security (pp. 785-799).
:::

## Background
:::spoiler [What is Adversarial Example? - 運用對抗例攻擊深度學習模型](https://medium.com/trustableai/%E9%87%9D%E5%B0%8D%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92%E7%9A%84%E6%83%A1%E6%84%8F%E8%B3%87%E6%96%99%E6%94%BB%E6%93%8A-%E4%B8%80-e94987742767)
> 所謂對抗例，是一種刻意製造的、讓機器學習模型判斷錯誤的輸入資料。最早是 Szegedy et al（2013）發現對於用 ImageNet、AlexNet 等資料集訓練出來的影像辨識模型，常常只需要輸入端的微小的變動，就可以讓輸出結果有大幅度的改變。例如取一張卡車的照片，可以被模型正確辨識，但只要改變影像中的少數像素，就可以讓模型辨識錯誤，而且前後對影像的改變非常少，對肉眼而言根本分不出差異。
:::

:::spoiler [hook（钩子函数）](https://blog.csdn.net/chehec2010/article/details/91360772)
[钩子函数是什么意思](https://www.zixuerumen.com/17234.html)
> 在Windows系統中一切皆消息，按鍵盤上的鍵，也是一個消息。Hook 的意思是鉤住，也就是在消息過去之前，先把消息鉤住，不讓其傳遞，使用戶可以優先處理。執行這種操作的函數也稱為鉤子函數。

[Hook API讓應用程式乖乖轉彎，駭客也是這麼做 ](https://www.fineart-tech.com/index.php/ch/news/699-fineartsecurity-apihook)
:::

:::spoiler [Remote Procedure Call (RPC) in Operating System](https://www.geeksforgeeks.org/remote-procedure-call-rpc-in-operating-system/)
> Remote Procedure Call (RPC) is a powerful technique for constructing distributed, client-server based applications. It is based on extending the conventional local procedure calling so that the called procedure need not exist in the same address space as the calling procedure. The two processes may be on the same system, or they may be on different systems with a network connecting them. 
---
在王凡老師的OS中也有提到RPC(Ch.3 P3.54)
> Remote procedure call abstract procedure calls between processes on networked systems

簡單來說，他可以執行遠端PC的某一個module或method，而這東西的好處是可以降低programmer學習IPC的障礙，因為這種方式更直觀，大概就像下圖一樣
![](https://media.geeksforgeeks.org/wp-content/uploads/operating-system-remote-procedure-call-1.png)
:::

:::spoiler [What is Class Hierarchy Analysis?](https://www.researchgate.net/figure/Example-Class-Hierarchy-Analysis-CHA-Our-Class-Hierarchy-Analysis-is-a-static-compile_fig1_269196977)
> It is a static (compile time) analysis that uses the class hierarchy to compute which method implementations can be invoked by objects of each class type. The left diagram above shows an example hierarchy of five classes where subclasses point to their parent class: D and E are subclasses of C while B and C are subclasses of A.
![](https://www.researchgate.net/profile/Zachary-Tatlock/publication/269196977/figure/fig1/AS:668907362856968@1536491351260/Example-Class-Hierarchy-Analysis-CHA-Our-Class-Hierarchy-Analysis-is-a-static-compile.png)
:::

[8 種主流深度學習框架介紹](https://blog.csdn.net/zw0Pi8G5C1x/article/details/121571055)
[[Day 21] 媽! Keras 和 TensorFlow 在亂存模型啦! ( TFLite 輕量模型) ](https://ithelp.ithome.com.tw/articles/10272501)

:::spoiler [What is OCR? - 文字辨識方法統整](https://d246810g2000.medium.com/%E6%96%87%E5%AD%97%E8%BE%A8%E8%AD%98%E6%96%B9%E6%B3%95%E7%B5%B1%E6%95%B4-1e3d3ba5fe54)
> OCR 英文全稱是 Optical Character Recognition，中文叫做光學字元識別，目前是文字辨識的統稱，已不限於文檔或書本文字辨識，更包括辨識自然場景下的文字，又可以稱為 STR（Scene Text Recognition）。
>
>圖1 中有三個大分類，包含 Text detection, Text recognition, Text spotting，Text detection 主要是偵測文字在影像中的哪個位置，Text recognition 主要是將偵測後的結果拿來辨識是什麼文字，而 Text spotting 則是將 detection 和 recognition 整合到一個 End-to-End 的網路中來進行文字辨識。
![](https://miro.medium.com/v2/resize:fit:720/format:webp/1*UxmtG_Y3E4NyZVeoGnD3OQ.png)
:::


[互聯網行業中，常說的API和SDK是什麼？](https://ithelp.ithome.com.tw/articles/10233788)

[What is Tiny Encryption Algorithm(TEA)?](https://www.jianshu.com/p/4272e0805da3)

[What is MACE framework? - 小米AI推理框架MACE介绍](https://blog.csdn.net/tugouxp/article/details/123262864)

:::spoiler [What is a trusted execution environment (TEE)?](https://www.techtarget.com/searchitoperations/definition/trusted-execution-environment-TEE)
> A trusted execution environment (TEE) is an area on the main processor of a device that is separated from the system's main operating system (OS). It ensures data is stored, processed and protected in a secure environment. TEEs provide protection for anything connected, such as a trusted application (TA), by enabling an isolated, cryptographic electronic structure and end-to-end security. This includes the execution of authenticated code, confidentiality, authenticity, privacy, system integrity and data access rights.
:::

:::spoiler What is Perturbation Budget? - From ChatGPT
> 在深度學習安全領域，擾動預算指的是可以引入到輸入數據中的最大擾動或失真程度，而不會顯著影響深度學習模型的輸出或預測結果。
>
>擾動通常作為對抗攻擊的一部分引入，攻擊者試圖以某種方式操縱輸入數據，使模型出現誤分類或產生錯誤輸出。通過設置擾動預算，系統可以限制這些攻擊的影響，並提高其對抗攻擊的魯棒性。
>
>擾動預算的定義方式因應用和攻擊類型而異。例如，它可以用擾動向量的L2或L∞範數來衡量，分別代表原始輸入數據和擾動後數據之間的歐幾里得距離或最大絕對差值。
>
>總的來說，擾動預算是評估深度學習模型安全性和魯棒性的重要參數，特別是在安全性是重要關注點的應用中。
:::

:::spoiler [What is quantization? - 使用機器學習解決問題的五步驟 : 模型推論](https://datasciocean.tech/machine-learning-basic-concept/machine-learning-model-inference/)
> Pruning 與 Quantization
>
>我們在這裡簡單說明 Pruning 與 Quantization 的概念，如果想更深入學習模型效能、速度與能耗的最佳化問題，可以參考 TensorFlow 的官方文件。
>
>Pruning : 全名為 Weight Pruning，中文稱為「權重修剪」。透過觀察模型中哪些參數對於模型的預測過程較沒有影響，將這些參數移除，達到降低模型複雜度與運算量的目的。
Quantization : 中文稱為「量化」。模型中的參數如果是 32-bit 的浮點數，將其轉為 8-bit。透過簡化模型中參數的「精確程度」達到降低模型體積並提高運算速度的目的。
不管是 Pruning 或是 Quantization，都是希望夠在簡化模型複雜度、提升運算速度並降低能源與時間消耗的同時，保持模型原來的預測準確度。
:::

[What is transfer learning?](https://youtu.be/qD6iD4TFsdQ)