---
title: How to Root Android Phone & Install AlwaysTrustUserCert.zip Module?
tags: [problem solution]

---

# How to Root Android Phone & Install AlwaysTrustUserCert.zip Module?
1. Install [adb & fastboot++](https://github.com/K3V1991/ADB-and-FastbootPlusPlus/releases)
2. 透過USB連接手機和電腦，如果測試`$ fastboot devices`發現沒有抓到連線的裝置可以到[Get the Google USB Driver](https://developer.android.com/studio/run/win-usb)下載最新的驅動，並且在裝置管理員的地方更新
    
## Android Studio Emulator
本方法完全是參考[Root an Android emulator with just one command](https://youtu.be/zZZVoUTZipw?si=-r7H1aWTeTDFkSOr)，很簡單而且成功率很高，如果有特殊的需求而需要使用Physical Device，再往下看其他的Physical Device的Rooted Method
1. 用Android Studio開啟Emulator
    請記住Emulator的API Level，以我的為例是31
    ![圖片](https://hackmd.io/_uploads/Hy2UPOFAR.png)
2. Download Script & Execute it
    到 https://gitlab.com/newbit/rootAVD 下載latest script
    ```bash!
    $ git clone https://gitlab.com/newbit/rootAVD
    $ cd rootAVD
    $ rootAVD.bat ListAllAVDs
    ...
    rootAVD.bat system-images\android-31\google_apis_playstore\x86_64\ramdisk.img
    rootAVD.bat system-images\android-31\google_apis_playstore\x86_64\ramdisk.img FAKEBOOTIMG
    rootAVD.bat system-images\android-31\google_apis_playstore\x86_64\ramdisk.img DEBUG PATCHFSTAB GetUSBHPmodZ
    rootAVD.bat system-images\android-31\google_apis_playstore\x86_64\ramdisk.img restore
    rootAVD.bat system-images\android-31\google_apis_playstore\x86_64\ramdisk.img InstallKernelModules
    rootAVD.bat system-images\android-31\google_apis_playstore\x86_64\ramdisk.img InstallPrebuiltKernelModules
    rootAVD.bat system-images\android-31\google_apis_playstore\x86_64\ramdisk.img InstallPrebuiltKernelModules GetUSBHPmodZ PATCHFSTAB DEBUG
    ...
    ```
3. 選擇適當的command
    可以從上面的output看到，API Level 31的所有commands，選擇第一個執行就可以了
    ```bash
    $ rootAVD.bat system-images\android-31\google_apis_playstore\x86_64\ramdisk.img
    ```
    等大約3-5分鐘後，Emulator會自動關機，此時選擇Cold Boot
    ![圖片](https://hackmd.io/_uploads/Sy__O_YCA.png)
    開啟後，會發現Magisk已經被安裝在Emulator上，點開Magisk之後會在5秒內重開機，此時所有程序應該就結束了，可以測試一下有沒有確實Root
    ```bash!
    $ adb shell
    emulator64_x86_64_arm64:/ $ ls /data/data
    ls: /data/data: Permission denied
    1|emulator64_x86_64_arm64:/ $ su
    emulator64_x86_64_arm64:/ # ls /data/data
    android                                                        com.android.simappdialog
    android.auto_generated_rro_product__                           com.android.simappdialog.auto_generated_rro_product__
    android.auto_generated_rro_vendor__                            com.android.soundpicker
    ...
    ```
## ASUS ZenFone 3(Z017DA)
這一台是Lab的手機，我拿到的時候就已經進入Bootloader了，所以我就直接跳到後半段，但是這一台應該是刷壞了，我先紀錄一下整個過程，現在是已經無線迴圈同一個畫面了QAQ
### Install Third Party Recovery
我是參考[給老手的 Zenfone 3 刷機快速上手（Bootloader, Recovery, Root, Rom…）](https://medium.com/ishengp-laboratory/zenfone-3-softmod-879377e4ba4e)
1. 我是以[OrangeFox](https://xdaforums.com/t/twrp-treble-zenfone3-official-orangefox-recovery-project-r10-0.3956604/)為例，因為如果實際去看[TWRP](https://twrp.me/Devices/)，會發現唯獨缺了ZenFone3的Img
2. 安裝方法是:
    1. 下載[OrangeFox Img](https://orangefox.download/zh-TW/device/zenfone3)
    2. 進入fastboot
        ```bash!
        $ adb reboot bootloader
        ```
    2. 確認fastboot有抓到device並且把recovery檔案丟進去
        ```bash!
        $ fastboot devices
        H7AZCY01Z728HGB fastboot
        $ fastboot flash recovery recovery.img
        Warning: skip copying recovery image avb footer (recovery partition size: 0, recovery image size: 31850496).
        Sending 'recovery' (31104 KB)                      OKAY [  0.726s]
        Writing 'recovery'                                 OKAY [  0.359s]
        Finished. Total time: 1.185s
        ```
    4. 此時，直接切換到Recovery模式(`音量鍵-` + `電源鍵`)，要按久一點，應該會回到一開始的頁面，也就是10秒內沒有選擇要去哪裡就預設Restart，此時要選擇去到Recovery的地方，那這樣我們就可以進入OrangeFox的系統
    5. 到這邊理論上都沒有什麼問題，但是我按照[這個影片](https://youtu.be/p1MgtWuvqTM?si=gi5vKJSCNeFRJrgh)提到的要把剛剛載的image zip檔案丟進去並且安裝，但是就會跑出如下錯誤:
        ![125588](https://hackmd.io/_uploads/rymaNviC6.jpg =200x)
        看了XDA的留言串，發現也有人有這個問題，雖然時間有點久，但我還是嘗試問看看該名網友有沒有找到解決方法
## HTC 10
### Unlock Bootloader
1. 註冊[HTCdev](https://www.htcdev.com/bootloader/unlock-instructions)
2. 選擇標的
    ![圖片](https://hackmd.io/_uploads/rJBd1bjAT.png)
3. 進入開發者模式
4. 啟動OEM解鎖
5. 關機
6. 按著音量鍵下 + 電源鍵進入Fastboot
7. 接上電腦後用前面安裝的fastboot++下指令
    ```bash
    C:\Program Files (x86)\ADB and Fastboot++>fastboot oem get_identifier_token
    (bootloader) [KillSwitch] : /dev/block/bootdevice/by-name/frp
    (bootloader) [KillSwitch] Last Byte is 0X01, enable unlock
    (bootloader)
    (bootloader) < Please cut following message >
    (bootloader) <<<< Identifier Token Start >>>>
    (bootloader) 5AD6E332F11F68FA4D0B820709F5F484
    (bootloader) F9FCA8C301C6479544B350B86652DCED
    (bootloader) F1D0D367B49E0446C9697859C05FD9DD
    (bootloader) DB74A5312EBBC6298DB8635F04BDDA2E
    (bootloader) 1BF5BB63E5B09F3C1DFD02004B705E22
    (bootloader) 0F3CF67C948A30217139C9CF8A5B71D8
    (bootloader) A6D9E15DC0EA30BDE41B6D2057737343
    (bootloader) B87E8C56B1C27FF7F1E7FE67703EDA32
    (bootloader) A6D17FA27764CF7FA8D9BF397860D64B
    (bootloader) 0E9EE351C663BCB6E21F8916723110E1
    (bootloader) F4398F6521FEF73F3F54CA8DAABD00A4
    (bootloader) 4D63AF96305C61EBD5F625CF64AC5558
    (bootloader) EA35A42E7F061B3E2D6D854A6F3DC204
    (bootloader) 336D9F145BC218986BAAAFCBE149A8C6
    (bootloader) 4D338857042EAE2224CB9EB1827EF86F
    (bootloader) A56D01AD0F5921E9A3F6A33FC9C287B6
    (bootloader) <<<<< Identifier Token End >>>>>
    OKAY [  0.175s]
    Finished. Total time: 0.176s
    ```
8. 回到剛剛的HTCdev網頁後按下一步，在下面貼上剛剛得到的Token
    ![圖片](https://hackmd.io/_uploads/rJLL-boCT.png =300x)
9. 沒意外的話他會寄送一封mail到註冊時填寫的email
    ![圖片](https://hackmd.io/_uploads/SyAqZ-jCp.png)
10. 把寄送的檔案放到fastboot++同一個資料夾後，直接在fastboot++下command
    ```bash
    $ C:\Program Files (x86)\ADB and Fastboot++>fastboot flash unlocktoken unlock_code.bin
    Sending 'unlocktoken' (0 KB)                       OKAY [  1.005s]
    Writing 'unlocktoken'                              (bootloader) flash unlocktoken
    (bootloader) [KillSwitch] : /dev/block/bootdevice/by-name/frp
    (bootloader) [KillSwitch] Last Byte is 0X01, enable unlock
    (bootloader) unlock token check successfully
    OKAY [  0.033s]
    Finished. Total time: 1.050s
    ```
11. 按下Enter之後，在手機端應該會出現要不要解鎖的訊息，直接用音量鍵選擇Yes並且用電源鍵確認就會直接解鎖了
### Install Third Party Recovery
我是參考[ How to Root the HTC 10 ](https://youtu.be/VubMLsETfpA?si=o4wVZP3LwP0jE-dh)
1. 直接去[TWRP - HTC 10](https://twrp.me/htc/htc10.html)下載img，然後按照上面的guidelines進行安裝
    :::info
    這邊記得是`$ adb reboot download`，和平常的reboot到bootloader不一樣喔
    :::
3. 下adb command
    ```bash!
    $ adb reboot download
    $ fastboot flash recovery twrp.img
    Warning: skip copying recovery image avb footer (recovery partition size: 0, recovery image size: 30965760).
    Sending 'recovery' (30240 KB)                      OKAY [  1.976s]
    Writing 'recovery'                                 (bootloader) HOSD CL#857212
    (bootloader) start@1
    (bootloader) recovery@100%
    (bootloader) Update partition OK
    (bootloader) end@Done
    OKAY [  2.774s]
    Finished. Total time: 4.765s
    $ fastboot reboot
    Rebooting                                          OKAY [  0.001s]
    Finished. Total time: 0.002s
    ```
3. 在手機端安裝Magisk並且在電腦端也下載同一個apk，接著進到TWRP Recover的地方，原本到這邊應該就直接在Install的地方進行安裝Magisk，但是就如同[阿哲的影片](https://youtu.be/AcWvTfdm1vE?si=uKtkbGuVElDvcaHO&t=1388)所說，這一台手機也是無法直接在TWRP進行安裝apk的，也是要用sideload才可以
    ```bash!
    $ adb reboot bootloader
    ```
4. sideload進行安裝
    在TWRP中點選Advanced，然後點選sideload並且wipe cache，下完command後點選reboot system後就結束了
    ```bash!
    $ adb sideload Magisk-v27.0.apk
    Total xfer: 3.01x
    ```
5. 測試
    ```bash!
    $ adb shell
    htc_pmeuhl:/ $ whoami
    shell
    htc_pmeuhl:/ $ su
    htc_pmeuhl:/ # whoami
    root
    ```
### 後記
因為要做實驗，也就是為了繞過SSL Pinning的問題要安裝==AlwaysTrustUserCerts==這個模組，所以magisk我是安裝
## SONY Xperia 10 III(XQ-BT52)
結論：這一隻root的過程還蠻順利的，但最後結果還是失敗，不是說root失敗而是出現wifi網卡不能用的情況，但只要連接SIM卡還是可以用的，但就跟我的研究沒關係了
### Unlock Bootloader
1. 在通話的地方輸入`*#*#7378423#*#*`就會進入工程機畫面
2. 選擇Service Info -> Configuration中會出現Bootloader unlock allowed: Yes(No)的提示，如果是Yes再往下進行
3. 接著回到電話播打處打上`*#06#`就會跳出IMEI Code
    ![Screenshot_20240322-212046](https://hackmd.io/_uploads/ryZRhZjCa.png =200x)
4. 到[Sony Unlock官網](https://developer.sony.com/open-source/aosp-on-xperia-open-devices/get-started/unlock-bootloader)，選擇手機的型號並且輸入剛剛得到的IMEI Code
    ![圖片](https://hackmd.io/_uploads/r1XUU-jCT.png)
    Submit後會給另外一個Code
    ![圖片](https://hackmd.io/_uploads/rkbKUWoAT.png)
5. 這一部分和哲有一點點不一樣，我是參考[Sony Xperia 10 V (XQ-DC72) Root教學，解鎖Bootloader與刷Magisk](https://ivonblog.com/posts/sony-xperia-10-v-root/)，先想辦法進入開發者模式後，開啟adb debugging並且開啟OEM解鎖，接著連接電腦重啟
    ```bash!
    $ adb devices
    List of devices attached
    HQ615A42D4      device
    $ adb -s HQ615A42D4 reboot bootloader
    $ fastboot oem unlock 0xF8E5B9BD1CA8816F
    OKAY [  3.969s]
    Finished. Total time: 3.973s
    ```
    
### 刷入修補過的boot.img
這一部分就幾乎都是看[ How to root Sony Xperia 10 V and flash Magisk ](https://youtu.be/CwGieZnmhPM?si=vqY5pszVesD2P8d3)
1. Install [XperiaFirm](https://xperifirm.com/category/download/)
2. 選擇自己的型號並且下載，下載完後他會自己解壓縮
    ![圖片](https://hackmd.io/_uploads/BkbF0x2C6.png)
3. 下載[sony_dump](https://xdaforums.com/t/tool-windows-linux-android-apple-unpack-any-sony-firmware-file.3530077/)並且把對應的電腦架構放到剛剛的下載的img folder(windows是sony_dump.exe)
4. 在該資料夾執行command，command後面接的檔案試不同型號會有不一樣的檔名，這點要特別注意
    ```bash!
    $ sony_dump.exe output boot_X-FLASH-ALL-8A63.sin
    --------------------------------------------------------
           Sony File Dumper by Munjeni @ 2016
    --------------------------------------------------------
    Using folder "output"
    opening boot_X-FLASH-ALL-8A63.sin
    boot_X-FLASH-ALL-8A63.sin is Sony sin v5 format.
    Extracting from boot_X-FLASH-ALL-8A63.sin
    Extracting file output/boot_X-FLASH-ALL-8A63.crt
    Extracting file output/boot_X-FLASH-ALL-8A63.000
    End of boot_X-FLASH-ALL-8A63.sin
    Done.
    ```
    執行成功後應該會在同一個folder中出現output這個folder，把裡面的第一個檔案改成.img file，並且丟到手機端
5. 在手機端安裝magisk後，用magisk安裝這個img，他會patch這個img
6. 成功後應該會在手機同一個folder底下看到patch過後的img file，此時就直接把該檔案再丟回到電腦端並且在同一個folder底下開啟terminal
    ```bash!
    $ adb devices
    List of devices attached
    HQ615A42D4      device
    $ adb reboot bootloader
    $ fastboot devices
    HQ615A42D4      fastboot
    $ fastboot flash boot magisk_patched-27000_k2w6q.img

    Sending 'boot_a' (98304 KB)                        OKAY [  2.167s]
    Writing 'boot_a'                                   OKAY [  0.237s]
    Finished. Total time: 2.423s
    $ fastboot reboot
    Rebooting                                          OKAY [  0.000s]
    Finished. Total time: 0.001s
    ```
    此時我們大致上就成功了，等待開機的時候會有一點久(約2-5分鐘不等)，請耐心等候
7. 測試
    ```bash!
    $ adb shell
    XQ-BT52:/ $ whoami
    shell
    XQ-BT52:/ $ su
    XQ-BT52:/ # whoami
    root
    ```
## SONY Xperia Z3
解鎖Bootloader的方法和上面一模一樣
## Install AlwaysTrustUserCert.zip Module
前面的手機取得Root權限後，就要安裝這個模組，我們才能部分Bypass SSL Pinning的問題，步驟如下
1. 在電腦下載[這個模組](https://github.com/NVISOsecurity/MagiskTrustUserCerts)，並且按照指示進行壓縮後丟到手機端
2. 並且把Zap的所有憑證準備好，通常如果只有一台裝置就會只有一個有效的憑證，但因為我有時候會桌電和筆電輪流切換，所以有兩個憑證
3. 先在手機安裝憑證(詳細上網找，資源很多，通常一分鐘內就可以安裝完成)
4. 安裝完了以後就在Magisk的Module分頁安裝剛剛壓縮的模組，如果沒意外的話應該會看到一個Reboot的按鈕，點擊後等重開機就完成了，如果安裝失敗可以看一下原因，我自己是遇到Magisk的版本需要更改
5. 重開機完成後可以看一下憑證的信任單位，應該就會看到安裝的ZAP所屬的OWASP被手機信任，在安裝模組之前一定是沒有的
6. 此時就可以測試，在電腦上開啟ZAP，然後把手機端的Proxy IP和Port設定好，理論上不管是手機端的瀏覽器封包或是部分App的流量就會被抓到

## 注意事項
:::info
有一點要特別注意，如果先安裝模組再進行安裝，或是先前已經安裝過第一個憑證後續又再安裝另外一個但沒有重起，會造成和之前遇到的SSL Pinning一樣的狀況，也就是在第二個憑證的裝置只能抓到GET封包，所以正確的步驟是按照上面的流程，如果有多一台裝置的話，最保險的做法是先把之前所有安裝的憑證刪除→重新啟動→重新安裝"所有"的憑證→重新安裝Magisk模組→Reboot，就可以了
:::
## 結論
最後只有HTC 10成功取得Root權限並且安裝`AlwaysTrustUserCert.zip`的模組，所以我的研究就圍繞在Google Pixel6a這一台原本已經Root好並且安裝好模組的手機以及HTC 10這一台