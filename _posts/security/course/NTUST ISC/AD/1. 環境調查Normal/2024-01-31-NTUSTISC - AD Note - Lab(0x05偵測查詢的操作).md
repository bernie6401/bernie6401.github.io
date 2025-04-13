---
title: NTUSTISC - AD Note - Lab(偵測查詢的操作)
tags: [NTUSTISC, AD, information security]

category: "Security/Course/NTUST ISC/AD/1. 環境調查Normal"
---

# NTUSTISC - AD Note - Lab(偵測查詢的操作)
<!-- more -->
[TOC]

Lecture Video: [2022/05/04 AD 安全1](https://youtu.be/Cv2gNQkDM8Q?si=SycYwgWohlu97dc3)

## Lab Time - 環境調查

### ==Lab - How to observe they've audited the record?==
像前面說的，如果在群組的user要觀察ad的name, description之類的，要如何觀察到他們正在做的事情?可以利用==Windows Event ID: 4662==，這個event ID會針對所有user對LDAP的查詢進行log，這樣不管是誰進行查詢都會留下紀錄，但是事先要啟用(預設不開)
1. GPO(Group Policy Object)啟動相關事件稽核
    在Win2016一開機會啟動Server Manager，其中的`Tools/Group Policy Management`
    ![](https://hackmd.io/_uploads/H1ZYPF7Rn.png)

    點選進去後在`Forest:kuma.org/Domains/kuma.org/Default Domain Policy`按右鍵選取Edit就會看到==Group Policy Management Editor==
    ![](https://hackmd.io/_uploads/H1bx_t7C3.png)
    
    接著在`Group Policy Management Editor/Computer Configuration/Policies/Windows Settings/Security Settings/Local Policies/Audit Policy`中可以找到==Audit directory service access Properties==，勾選起來就可以了
    ![](https://hackmd.io/_uploads/ByynOtmC3.png)

2. 使用者管理開啟進階功能
    * 接下來要設定哪些使用者的這些行為要被稽核，首先打開Windoes Startup中有一個==Active Directory Users and Computers==
    ![](https://hackmd.io/_uploads/rJxddjPp3.png)
    * 進入View中把Advanced Features功能打開
    ![](https://hackmd.io/_uploads/ryIsdow6n.png)
    * 接著左邊的列表會出現一些東西，包含Users，我們右鍵Users選擇屬性，並進入Security/Advanced/Auditing
    ![](https://hackmd.io/_uploads/HJexFjDp3.png)
    * 進行新增，最上面的Principle直接打Everyone就可以了，代表任何人，下面的Permission勾選`List Contents`
    ![](https://hackmd.io/_uploads/S1I8KswT3.png)
    * 這一連串的操作就代表，任何人只要在kuma這個網域底下進行List Content的操作，AD DC都會偵測到進行紀錄
        :::spoiler Result
        ![](https://hackmd.io/_uploads/Hy8yjiDTh.png)
        稍微解釋一下，做邊是kuma.org網域的bear帳戶，在右下角有顯示時間為12:37，此時進行`net user /domain`的操作，而右邊是DC，我們利用Event Viewer進行查看Event ID: 4662中的確記錄到此次event，而查詢的帳號也的確是bear
        :::

---