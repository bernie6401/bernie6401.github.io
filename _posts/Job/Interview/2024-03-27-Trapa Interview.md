---
title: Trapa Interview
tags: [Interview]
category: "Job｜Interview"
---

# Trapa Interview
<!-- more -->

## 面試流程

### 一面
* (1HR)一面主要是[ddaa](https://twitter.com/0xddaa)主面，人非常的好也很願意給我建議和修正的地方，一開始主要針對公司在開發的平台以及整體公司現況做簡單的說明，接著就直接進到自我介紹，完了之後開始針對自我介紹的內容做非~常~詳細的詢問，諸如目前實習的地方主要是在幹麻、開發的東西是什麼、IPS和Firewall的品牌是什麼之類的(因為我主要是針對公司內部開發一個防火牆的整合系統所以會被問這個東西)，還有針對我寫的各種文章、藍隊的題目靶機(BTLO、Cyberdefenders)有沒有印象深刻的題目、以及針對比賽的經驗、有沒有什麼特別令人印象深刻的地方或是題目是很有成就感的(因為我跟他說參加過去年和今年的EOF，所以針對決賽的A&D以及KoH會比較多問題)等等，總之這一段我個人認為就是閒聊，主要了解我的個人經歷以及目前的經驗到哪裡，但是還是那句老話，自己的經驗有多少寫多少，不要不是自己做的也寫上去，不然被問爆就會露出馬腳
* 緊接著沒記錯的話就是問一些比較和資安專業的問題(這一個階段是在不上網Google的情況之下以自己本身的經驗和知識回答)，我記得的題目有
    1. 什麼是Mitre ATT&CK
    2. SOC團隊主要是幹嘛的
    3. 有沒有什麼特別印象深刻的APT攻擊
    4. 什麼是IDS、IPS、EDR、MDR
    
    最後一題答的非常不好，應該說我之前有接觸過但真的一時忘記的，所以就只能交給ddaa幫忙改正我的答案，這邊再寫一次好了，以免忘記
    1. IDS(Intrusion Detection System, 入侵偵測系統)
        從名字就可以看的出來，他是針對流入流出的各種封包的偵測系統，也就是獨立於Firewall的旁之，如果他有檢測到封包內有什麼異常的Payload或是pattern，就會跳出告警，但就僅只於此，不會再做更多的操作
    2. IPS(Intrusion Prevention System, 入侵防禦系統)
        IPS就是要改進上述的問題，他主打的就是偵測到快快的東西就會主動的防禦掉，但這樣還是有一個問題，現今的攻擊手法越來越多種，而且有時候是那種可以包裝成安全落地的形式，必須要在本地端監控才有辦法知道
    3. EDR(Endpoint Detection and Response, 端點偵測與應對)
        EDR就是在做這樣的事情，可是有可能會有一個疑問，每個人的主機內不是都有安裝那種傳統的Windows Defenders或是小紅傘那種東西，為什麼還需要有EDR，其實現今的攻擊手法已經有很大的變化，有可能單純看個人的裝置會看不出個所以然，必須要聯合其他的裝置一起做關聯性的比對才會知道目前是不是正在遭受攻擊，所以EDR強大的地方在於他做到各個裝置endpoint端點的串聯，讓資安事件的偵測和防禦可以更嚴謹，這也是中小型企業最需要的資安產品
    4. MDR(Managed Detection and Response, 受管式偵測與應對)
        這東西其實就是一個EDR+SOC的服務衍生的產品，但ddaa說這個東西要做出市場區隔可能還沒有到太創新
* (1HR)緊接著就是人生第一次的白板題，題目敘述如下:
    有一個遊戲，規則是有一個炸彈，炸彈上有好幾條線，每一條線都有三個特徵，我必須根據這三個特徵判斷文氏圖並且決定要不要剪斷這一條線，文氏圖如下，這是我從網路上找到最像題幹的圖片
    ![venndiagram](https://hackmd.io/_uploads/HkQnldw6p.png)
    剛剛講到每一條線的三個特徵分別是: 線的一端連接的LED有沒有亮、該條線的顏色(是否為紅或藍或非藍也非紅或是同時是藍也是紅)、線的另外一端有無標示星號，依照上圖來說，A區域就是有無星號、B區域是LED有無亮、C區域是線是紅色、D區域是線是藍色，所以假設現在有一線的三個特徵是有LED、有星號且是紅色，則我們應該要圈A、B和C，最後的交集就是44和32，當然當時的題目不是這些數字，他是有代號的，共有五個C、D、S、P、B，分別代表:
    C: 無條件剪斷線
    D: 暫時先不要剪斷，根據搭配到的其他代號(S、P、B)進行後續驗證
    S: 如果炸彈的序列號為偶數則剪斷線
    P: 如果炸彈有Port號也要剪斷線
    B: 如果炸彈的電池有兩個以上也要剪斷線
    
    總結一下上述的問題:
    Input: 線的三個特徵(LED亮暗或閃爍、線的顏色、有無星號)以及炸彈的三個特徵(序列號、電池數量、Port號)
    Output: 根據以上的狀態判段該條線要不要剪斷
    
    以下附上我的Source Code:
    :::spoiler Source Code
    ```python
    try:
        led_light = input("LED Light Or Not Or Flashing (Y/N/F): ").upper()
        assert led_light == "Y" or led_light == "N" or led_light == "F"
        if led_light == "F":
            led_light = "N"
        star_or_not = input("Star Or Not (Y/N): ").upper()
        assert star_or_not == "Y" or star_or_not == "N"
        cable_color = input("Cable Color (R/B): ").upper()
        assert cable_color == "R" or cable_color == "B"
        bomb_feature_serial = int(input("Bomb Feature Serial (number): "))
        assert bomb_feature_serial >= 0
        bomb_feature_port = int(input("Bomb Feature Port (number): "))
        assert bomb_feature_port >= 0
        bomb_feature_battery_num = int(input("Bomb Feature Battery Number (number): "))
        assert bomb_feature_battery_num >= 0
    except ValueError:
        print("Please input the correct value")
        exit()

    def judge_venn_diagram(led_light, star_or_not, cable_color):

        if led_light == "Y":
            if star_or_not == "Y":
                if cable_color == "R":
                    return "D", "B"
                elif cable_color == "B":
                    return "D", "P"
            else:
                if cable_color == "R":
                    return "B", "S"
                elif cable_color == "B":
                    return "P", "S"
        elif led_light == "N":
            if star_or_not == "Y":
                if cable_color == "R":
                    return "C", "P"
                elif cable_color == "B":
                    return "P", "D"
            else:
                return "S", "D"

    def judge_digit(digit):
        if "D" in digit:
            if "S" in digit:
               return judge_bomb_feature_serial(bomb_feature_serial)
            elif "P" in digit:
                if bomb_feature_port:
                    return True
                else:
                    return False
            elif "B" in digit:
                return judge_bomb_feature_battery_num(bomb_feature_battery_num)

        elif "C" in digit:
            return True

    def judge_bomb_feature_battery_num(bomb_feature_battery_num):
        if bomb_feature_battery_num >= 2:
            return True
        return False

    def judge_bomb_feature_serial(bomb_feature_serial):
        if bomb_feature_serial % 2 == 0:
            return True
        return False

    def main():
        print("Start Game")
        num1, num2 = judge_venn_diagram(led_light, star_or_not, cable_color)

        if judge_digit([num1, num2]):
            print("Cut")
        else:
            print("Don't Cut")  


    if __name__ == "__main__":
        main()
    ```
    :::
    當時是依照CodePilot和ChatGPT生出一些關鍵的語法再加上我自己的邏輯寫出來的，其實這一題算是簡單，我的留程是先借由線的三個特徵判斷文氏圖會圈出哪兩個字母(每一次一定都會圈出兩個字母，且C和D這兩個互斥的情況不會出現，一定是C或是D搭配SPB其中一個字母)
    :::info
    這邊要特別再說明一下，如果是閃爍就視為暗，如果LED沒有亮就代表我在圈文氏圖的時候要用排斥的角度看他，舉例來說如果LED沒亮、但是有星號且線為紅色，B圈到的部分就不能算，所以以上圖來說就會是420和432這兩個數字，如果是LED沒亮也沒有星號且線為紅色，則圈出來的部分就是1058和485這兩個數字，不知道這樣的說明夠不夠清楚
    :::
    總之，這個階段就需要不斷的和面試官來回詢問和溝通Spec的要求，我問了超多問題，例如: 閃爍的時候算不算一個新的狀態因為原本的Spec上沒有提到，結果ddaa說當成暗；剛開始的時候也對這個題目很矇，想說到底在衝三小，所以我直接問有沒有什麼是比較好的方式可以判斷文氏圖圈出哪些字母，ddaa說可以直接用if-else判斷就好，這也讓我有個底，如果只是利用到if-else，那題目應該不會很難，至少我是個會把問題複雜化的人，所以我在寫的時候就直接用最暴力的方式，就用巢狀if-else判斷所有狀態；我還問了上面特別提到的問題，如果特徵是否定的情況要怎麼處理，其實也就是要用排除的方式看待他等等問題，最後的結論是有寫出來，方向也大致上和ddaa預想的差不多，只是有一些小陷阱和可以改進的地方
    1. 陷阱就是我沒有考慮到非藍也非紅以及既是藍也是紅的這兩種情況，所以我判斷文氏圖的地方還缺了八個狀態沒有寫到，我會出現這個錯誤是因為Spec沒有寫這個東西，不過ddaa在一開始敘述題幹的時候有用一句話帶過，當時應該要稍微留心一下這個問題，只能說有時候Spec上的東西不會寫出全部的東西，還是需要透過不斷的和面試官溝(套)通(話)，才有機會避開這些陷阱
    2. 我想說這是一個遊戲，所以會需要有input給玩家輸入前面提到的六個狀態，但是ddaa說在業界我們不會這樣設計，在一開始寫code之前就會設定好用file的方式餵進去script中，只是要設定好資料的format
    被稱讚的地方: 流程清楚也符合邏輯、會針對input的資料進行檢查、最重要的是會和需求方不斷的溝通不同狀態下應該要有什麼樣的要求，這件事在業界是很重要的
* (20Min)白板題結束之後還有檢討一下，之後就要稍微進入問答，包含展示了目前公司開發的各項產品以及功能，並實際demo出來，要針對公司方面的問題也可以在這個階段提問


總體而言大概就是這樣

### 二面
首先因為已經過了一天，記憶有點遺失，就邊寫邊回憶，當天流程是會先和主管一對一的面談，面談過程會互相丟問題，讓用人單位更理解我的能力在哪裡，接著就是針對公司的現況和產品做簡單的介紹，當天面我的是Jeff
1. 其實就跟上次一面的狀況很像，簡單的自我介紹，過程中時不時會丟出一些更詳細的問題，包含實習的內容(弱密碼掃描這個Project被問到有沒有玩過一些進階的功能或是可能可以做什麼樣的改善，我回答可以針對Wordlist做到Augmentation，Jeff說方向正確，但hashcat原本就有這個功能，預設不開，需要下一些rule讓他可以做到Wordlist的Permutation，聽說效果超群)
2. 針對比賽也有聊到一些，例如今年和去年的EOF賽制不一樣，針對這一點我有大概解釋主辦單位的考量以及這個規則的缺點。還有，Jeff也問到這幾次比賽下來沒有得名的原因可能有什麼，除了賽制問題我也有提到經驗不足等等原因
3. 還有問到有哪個Project是目前做過最有成就感?(有點忘記了)，我回答大學的專題，也就是結合臉部情緒以及肢體情緒做整合的系統，還問到中間遇到什麼特別的挑戰
4. 平常的興趣或是如何排解壓力
5. 紙筆測驗: 有問到一些和網路相關的問題，我又說我是網管，所以就有紙筆測驗，題目是: 現在有一個通外網的服務、Intranet(開發的)、內部的服務，這三個網段分別需要怎樣的部署，或是和外網通或不通，我的結論如下圖
    ![117157](https://hackmd.io/_uploads/SJPXvGWJR.jpg)
    首先外網服務一定要有WAF，外到內首先會有Firewall和IPS，接著接上Router，然後DMZ通常接收Request和送出Response都是同一個Session，所以和外網是一條獨立的連線；而Intranet和DMZ則是單向通，並且Intranet也有上網的服務，所以會有一條通出去，但是會和回傳回來的Response錯開所以會有兩條；最後是內部Service Internet和DMZ也是單向通，而和Intranet則是有選擇的通，因為還是要看實際案例要怎麼樣的部署，不然如果兩邊都正常通就沒有必要切出兩塊了
6. 還有問到去年底參加的SOC課程(和中華資安的那個)學了什麼
7. 有無多人開發的經驗、會不會用Git(我回答3人以上的沒有，但會用基本的Git)
8. 有無管理3人以上的專案，不限課業上的也沒關係，我回答大學辦的電機營大約有100人左右，期間遇到的問題以及我怎麼解決的
9. 有問到工作的期待、環境等

## 結論
Offer保留到我畢業(我提議的)，期間也可以保持聯絡，並且Jeff建議我的觀念大部分都很OK，就是經驗缺乏，所以可以多刷一些Leetcode和[Hacker Rangers](https://hackerrangers.com/)