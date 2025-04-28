---
title: 'What is DevOps, MLOps, CI/CD?'
tags: [名詞解釋]

category: "Terminology"
---

## [什麼是 DevOps？](https://ithelp.ithome.com.tw/articles/10184557)
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

## [什麼是MLOps？-30 Days of MLOps](https://ithelp.ithome.com.tw/articles/10238335)
:::spoiler 
> 用最短的一句話來解釋它的話，MLOps 就是 Machine Learning 的 DevOps
> 在 Machine Learning 團隊中，除了資料科學家、資料工程師、DevOps 工程師作為固定班底外，協作單位還有產品經理、後端工程師等等。我們要讓所有人可以彼此良好的協作，這需要依賴更好的維運架構。除了最直覺想到的 Model 部署外，常見的挑戰還有例如：訓練 Model、測試與分析 Model、資料的預處理等等。
> ![](https://github.com/alincode/30-days-of-mlops/raw/master/assets/mlops-collenges.png)
* [CI/CD是什麼？一篇認識CI/CD工具及優勢，將日常瑣事自動化](https://www.wingwill.com.tw/zh-tw/%E9%83%A8%E8%90%BD%E6%A0%BC/%E9%9B%B2%E5%9C%B0%E6%B7%B7%E5%90%88%E6%87%89%E7%94%A8/cicd%E5%B7%A5%E5%85%B7/)
:::spoiler

## What is CI/CD
> CI/CD工具也是為了此概念(DevOps)而產生的自動化工具，透過持續整合、持續部署的方式，在開發階段就自動協助開發人員偵測程式碼問題，並部署至伺服器
>
> ---
> ### CI（Continuous Integration）持續整合
> 持續整合（Continuous Integration，CI）顧名思義，就是當開發人員完成一個階段性的程式碼後就經由自動化工具測試、驗證，協助偵測程式碼問題，並建置出即將部署的版本（Build）
> ### CD（Continuous Deployment）持續部署
> 持續部署（Continuous Deployment）可以說是CI的下一階段，經過CI測試後所構建的程式碼可以透過CD工具部署至伺服器，減少人工部署的時間。
>
> ---
> ### CI/CD工具1：GitHub 
> GitHub是眾所皆知的Git Server網站，其CI/CD服務稱為GitHub Action，提供了多項控制API，能夠幫助開發者編排、掌握工作流程，在提交程式碼後自動編譯、測試並部署至伺服器，讓每位開發者都能受惠於平台本身自有的CI/CD功能。
> ### CI/CD工具2：GitLab 
> GitLab主要的服務是提供git版本控制系統，其CI/CD Pipeline功能簡單又實用，使用者只需要設定於專案根目錄下的「.gitlab-ci.yml」檔，便可以開始驅動各種Pipeline協助您完成自動化測試及部署。目前有提供GitLab CE（社群版）與 GitLab EE（企業版）兩種，使用者可以根據自己的需求選擇適合不同的方案。
> ### CI/CD工具3：Anthos 
> 由Google所推出的Anthos是一款能幫助企業迅速部署混合雲架構的跨雲管理平台。若是企業資源龐大且分佈於多雲環境，每一次的更新與維護都需要針對不同架構調整，將會大幅提升管理應用程式的負擔，而透過Anthos便可以將複雜的多雲環境以統一形式呈現，加速開發人員管理應用程式，一次完成多雲部署，建立更敏捷、高效的應用程式維運環境。

## CI/CD VS DevOps
From ChatGPT:
簡單來說，**DevOps** 和 **CI/CD** 是有關聯但範圍不一樣的概念：

- **DevOps**（Development + Operations）是一個**文化**、**理念**、**做事方法**，目標是**促進開發（Dev）和運維（Ops）團隊合作**，加速產品從開發到部署的流程，讓軟體能更快、更穩定地交付。
  - 內容可以很廣，包括：自動化部署、基礎設施即程式（IaC）、監控、回報機制、團隊溝通等等。
- **CI/CD**（Continuous Integration / Continuous Delivery or Deployment）則是**實現DevOps目標的一組具體技術流程**。
  - **CI（Continuous Integration）**：持續整合，指的是開發人員經常（一天多次）將程式碼推送到版本庫，並透過自動化建置、測試，確保每次提交都是穩定的。
  - **CD（Continuous Delivery / Deployment）**：
    - **Delivery**：持續交付，指的是程式碼通過測試後可以**隨時**部署到生產環境，只是可能還要人手下指令。
    - **Deployment**：持續部署，則是程式碼一通過測試就**自動**部署到生產環境，不需人工干預。
    簡單一句話總結：
- **DevOps** 是一個大範圍的文化跟目標，**CI/CD** 是實現這個目標的方法和工具之一。