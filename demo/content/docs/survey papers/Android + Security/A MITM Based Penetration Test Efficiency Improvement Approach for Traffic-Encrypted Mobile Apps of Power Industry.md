---
title: A MITM Based Penetration Test Efficiency Improvement Approach for Traffic-Encrypted Mobile Apps of Power Industry
tags: [NTU, Meeting Paper]

---

# A MITM Based Penetration Test Efficiency Improvement Approach for Traffic-Encrypted Mobile Applications of Power Industry
:::info
Zhang, L., Wang, B., Shen, Q., Song, Y., Guo, N., & Xie, L. (2021, April). A MITM Based Penetration Test Efficiency Improvement Approach for Traffic-Encrypted Mobile Applications of Power Industry. In 2021 IEEE 6th International Conference on Computer and Communication Systems (ICCCS) (pp. 743-747). IEEE.
:::
這一篇蠻有趣的，和我想要做的東西幾乎一樣，不過他論文闡述的重點不一樣，但也還是給我一些之後需要注意的地方，

## Introduction
他是站在電力相關的Android App的角度去審視如果利用MITM Based做到滲透測試要怎麼做，以及和傳統的方式相比可以減少多少時間、效率提升多少。但其實內文和電力幾乎一點關係也沒有，代換成其他的App也可以，如果我們要利用MITM Based做到Penetration Testing，就必須要手動克服中間會加密的問題，所以他就試圖提出一個==3-Layers Proxy Based==的東西(如下圖)
![圖片](https://hackmd.io/_uploads/B1TUn8oGA.png)
從上圖可知，手機到Web Server中間總共有三層的Proxy，第一和第三層都是MITM Proxy，主要是負責訊息的加解密，而中間的那一層就可以很彈性的替換成各式各樣的自動化測試工具或腳本，例如Burp Suite或是SQLMAP之類的
:::info
這個架構會需要三層其實是因為他所測試的App，不只是傳輸的那一層會被SSL加密，而在傳送的封包body還會再加密一次，所以需要三層，不然照理來說，一層的MITM Proxy就可以解決SSL加解密的問題，不需要用到三層那麼多，而且也不需要深入探索他用的是哪一套加解密演算法，因為傳輸層的演算法都一樣才對，這是和學長討論出來的結果
:::
## Proposed Method
* First Layer Proxy: Mitm1
    ![圖片](https://hackmd.io/_uploads/ryZzTLofA.png)
    從上圖來看第一層的Proxy在Request的時候會負責解密從手機端加密的訊息，在傳遞Plaintext給第二層的腳本；而在Response則會反過來，他會把第二層提供的Plaintext加密回去再送給後面的手機
* Third Layer Proxy: Mitm2
    ![圖片](https://hackmd.io/_uploads/SJqj68ozA.png)
    上圖就是把response和request要做的事情反過來而已
## Experiment
* 重要事項:
    加解密的腳本需要事先準備好，意即我們要先確定該App是用哪種方式做到加解密，所以我們需要做到App的逆向工程，論文中有提到在電力工業中會用到的幾種方式:
    * MD5
    * AES
    * RSA
    * SM1-SM4
* Test Result W/o Automated Tools
    ![圖片](https://hackmd.io/_uploads/BJsiA8of0.png)
    ![圖片](https://hackmd.io/_uploads/S1QkJDofC.png)
    從上面兩張圖片可以知道response和request在明文的情況下，實際的封包內容為何，如果要進一步的測試的話，可以直接手動在body中間塞一些東西
    ![圖片](https://hackmd.io/_uploads/Hkp41DiMA.png)
    ![圖片](https://hackmd.io/_uploads/Hk-ryvjGA.png)
    在文章中他是在其中一個地方塞了單引號，也就是試圖引發sqli的效果
* Test Result W/ Automated Tools
    內文中說到這個不是本次研究的重點，所以指示確定他會正常動作就結束了
    ![圖片](https://hackmd.io/_uploads/SJXJxDsfR.png)
* 整體效率提升多少
    ![圖片](https://hackmd.io/_uploads/rkCVzwjzR.png)
    從上圖來看，傳統手動的方式進行加解密會很花時間，內文有提到:
    > 測試時間顯著縮短了96%左右。理論上，手動方法的測試時間等於加解密時間加上腳本和工具切換時間
    > 對於手動方法，大部分時間都浪費在不同工具之間的切換上
## Future Work
因為MITM Proxy適合支援HTTP和HTTPS協定的加解密，所以未來如果可以針對IoT設備的[MQTT協定](https://resource.webduino.io/blog/mqtt-guide)以及工控常用的[Modbus協定](https://www.dusuniot.com/zh-TW/blog/what-is-the-modbus-protocol-and-how-does-it-work/)，則coverage會更大
