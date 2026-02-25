---
title: "VirtualBox滑鼠無法跳出"
tags: [problem solution]

category: "Problem Solutions｜Others"
date: 2024-01-31
---

# VirtualBox滑鼠無法跳出
## Problem Description
在VirtualBox中如果滑鼠無法跳回本機，請先按照其他blog提出的solution自行排除[^vb-mouse-solution-csdn][^vb-mouse-solution-huawei][^vb-mouse-solution-baidu]，如果暫時找不到解決辦法，也可以參考[^vb-mouse-solution-moa]的做法，Ctrl+Alt+Del強制本機電腦跳出windows選項，此時滑鼠的控制權就會交回到本機端
<!-- more -->

## Solution
我的狀況是鍵盤是新買的小鍵盤，所以沒有Right Ctrl可以用，只有左邊，而且安裝增強功能VirtualBox會一直跳出"無法掛載映像檔"的字樣，最後是參考[^vb-mouse-solution-jinnsblog]中下面有一半教學是示範linux遇到這個問題要如何解決，簡單說就是手動在控制器的地方加入光碟機，並且選擇VBoxGuestAddition.iso，之後重開機就可以了

![](https://hackmd.io/_uploads/rJc9d3Sp3.png)

之後在VM的主視窗中選擇<span style="background-color: yellow">>插入Guest Additions CD映像檔</span>，就可以在系統中看到CD被掛載上去了，只要按照一般的安裝流程在reboot就可以解決滑鼠自由移動的目的了

![](https://hackmd.io/_uploads/SJjrYhrT2.png)

![](https://hackmd.io/_uploads/r1R5Y3H63.png)

## Reference
[^vb-mouse-solution-csdn]:[VirtualBox中鼠標在主機和虛擬機之間切換](https://blog.csdn.net/lijun5635/article/details/8715915)
[^vb-mouse-solution-huawei]:[在Windows虛擬機中安裝Virtualbox增強功能](https://support.huaweicloud.com/bestpractice-ims/ims_bp_0010.html)
[^vb-mouse-solution-baidu]:[ oracle vm virtualbox 怎麽讓鼠標出來啊？ ](https://zhidao.baidu.com/question/280635794.html)
[^vb-mouse-solution-moa]:[ [VirtualBox] windows下解決移除Host鍵後VM滑鼠無法移出 ](https://blog.moa.tw/2012/08/virtualbox-windowshostvm.html)
[^vb-mouse-solution-jinnsblog]:[Virtualbox Guest Additions 安裝教學 [Linux / Windows]](https://www.jinnsblog.com/2021/05/virtualbox-guest-additions-install-guide.html)