---
title: PicoCTF - No way out
tags: [PicoCTF, CTF, Reverse]

category: "Security｜Practice｜PicoCTF｜Reverse"
date: 2024-01-31
---

# PicoCTF - No way out
<!-- more -->

## Background
C Sharp / dn.spy / cheat engine

## Recon
大概有三種解法，其中兩種是改變.dll中的內容，有點利用binary exploitation的方式顯示flag，另外一種就是利用cheat engine的方式找到儲存座標的memory然後手動改寫數值，就拿到flag

## Exploit

### Method 1 - Change .dll
1. 可以看到`No way out/pico_Data/Managed/Assembly-CSharp.dll`可能是一個可以用dn.spy decompile的文件，先看看有沒有甚麼可以更改的
2. 在APTX class中，一個Mysterious的member，而且當`collision.gameObject == this.player`是true的時候，`this.Mysterious.SetActive(true);`就會被trigger，所以這就有點像是我們在遊戲中，如果要碰到白色旗子的時候會觸發的statement，那如果我在初始化的階段就直接把`this.Mysterious.SetActive(true);`設定成true，是不是就可以直接拿直到flag?
![](https://hackmd.io/_uploads/rylVM-rah.png)
3. Implementation
直接右鍵edit class變成多加一個Start() method，然後不用任何的條件就達到剛剛說的效果，切記一定要是Start，因為Start是有被實際呼叫的method，如果取個aaa這種名字，他本來就不會被呼叫，那改成這樣也沒意義，當然，也可以取其他會被呼叫到的method name，例如Update, Awake之類的
![](https://hackmd.io/_uploads/rJ-UNZBp3.png)

    ![](https://hackmd.io/_uploads/Hy_pE-HT2.png)


### Method 2 - Change .dll
當然記得能改動.dll的method，我們也可以改變遊戲角色跳不過圍牆的問題，最直觀的作法是我可以直接無限制的往上跳，超過圍牆就抵達flag，不會只有跳一小段這個問題，可以查看一下`EvolveGames/PlayerController/Update()`這個method，其中的第51行
```csharp!
if (Input.GetButton("Jump") && this.canMove && this.characterController.isGrounded && !this.isClimbing)
{
    this.moveDirection.y = this.jumpSpeed;
}
```
如果改成
```csharp!
if (Input.GetButton("Jump"))
{
    this.moveDirection.y = this.jumpSpeed;
}
```
跳躍的時候他就會沒有限制的增加z軸，這樣就可以翻牆拿到flag

### Method 3 - Cheat Engine
這個方法最有趣也最直接，還不用通靈，首先用cheat engine attach上遊戲的process
![](https://hackmd.io/_uploads/ByH3KIVpn.png)
然後我們假設座標的變數應該是float type，但是我們不知道初始值是多少，所以選Unknown initial value，scan下去會發現有230451200個value founded，所以可以藉由改變現有的遊戲狀態，篩選出座標的memory
![](https://hackmd.io/_uploads/rydgc8VTn.png)

* Move Forward
理論上這應該會讓座標的value增加，所以要選increased value
![](https://hackmd.io/_uploads/r1kxsdVTn.png)
* Move Backward
理論上這應該會讓座標的value增加，所以要選increased value
![](https://hackmd.io/_uploads/S1RgsONT3.png)
* Stay
選Unchanged value並勾選repeat
![](https://hackmd.io/_uploads/SJzJjdNah.png)

一直持續到最後會發現只有30多個，不斷嘗試disable那些memory就會發現有一個是儲存位置的，只要把那個memory改成任意座標，理論上我們就會跳過去，例如改成12，重新回到遊戲就會出現在flag附近，就可以拿到flag了
![](https://hackmd.io/_uploads/S1QkRdVa3.png)
![](https://hackmd.io/_uploads/B1qMJFNp2.png)

Flag: `picoCTF{WELCOME_TO_UNITY!!}`

## Reference
[^pico-reverse-no-way-out-wp-martin]:[ picoCTF 2023 No Way Out ](https://youtu.be/XzHJir0vtOk?si=U9RWOVUSnoQ9NEpw)
[^pico-reverse-no-way-out-wp-cryptocat]:[ Teleporting Through Walls with Cheat Engine - "No Way Out" [PicoCTF 2023] ](https://youtu.be/QgF4PQjeG-o?si=OBHfUigE0J1rT9jw)