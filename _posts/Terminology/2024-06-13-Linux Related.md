---
title: Linux Related
tags: [名詞解釋]

category: "Terminology"
date: 2024-06-13
---

## root folder底下的folder
```bash
/
├── bin     # （Binary）👉 基本指令執行檔
├── boot    # 👉 開機相關檔案
├── dev     # （Device）👉 所有裝置在 Linux 都是檔案
├── etc     # （Editable Text Config）👉 系統設定檔
├── home    # 👉 一般使用者家目錄
├── lib     # 👉 系統函式庫（Shared Libraries）
├── lost+found # 👉 檔案系統修復用目錄（超重要）
├── media   # 👉 掛載用
├── mnt     # 👉 掛載用
├── opt     # 👉 第三方軟體
├── proc    # （Process）👉 虛擬檔案系統（超重要）
├── root    # 👉 root 使用者的家目錄
├── run     # 👉 存放系統「開機後才存在」的暫時性執行資料
├── sbin    # （System Binary）👉 系統管理指令
├── snap    # 👉 Snap 套件系統使用的目錄
├── srv     # 👉 Service Data 目錄
├── sys     # 👉 kernel 與硬體資訊（sysfs）
├── tmp     # 👉 暫存檔
├── usr     # （Unix System Resources）👉 大部分應用程式放這
└── var     # （Variable）👉 會變動的資料
```

* /bin
    放的是：ls, cp, mv, cat, bash
* /sbin
    ```
    /usr/sbin/reboot
    /usr/sbin/fsck
    /usr/sbin/mount
    /usr/sbin/ip
    ```
    通常 root 才會用。
* /boot
    * Linux kernel
    * initramfs
    * grub 設定

    例如：
    ```
    /boot/vmlinuz
    /boot/grub/
    ```
    如果這壞掉 → 系統開不起來。
* /dev
    ```
    /dev/sda      硬碟
    /dev/null     黑洞
    /dev/random   隨機數
    /dev/tty      終端機
    ```
* /etc
    ```
    /etc/passwd
    /etc/shadow
    /etc/hosts
    /etc/ssh/sshd_config
    ```
* /home
    
    你自己的檔案都在這裡。
    ```
    /home/alice
    /home/bob
    ```
* /lib

    程式執行時會載入這些。你在做 pwn 時常會碰到 `libc`
    ```
    /lib/x86_64-linux-gnu/libc.so.6
    ```
* /usr
    ```
    /usr/bin
    /usr/lib
    /usr/share
    ```
* /var

    做取證會常看這裡。
    ```
    /var/log
    /var/log/auth.log
    /var/log/syslog
    /var/www
    /var/lib
    ```
* /tmp

    任何人都能寫。通常會定期清空。很多惡意程式會丟 payload 在這。

* /proc
    
    pwn 會常用。
    ```bash
    /proc/1
    /proc/self
    /proc/cpuinfo
    /proc/meminfo
    $ cat /proc/self/maps
    ```
* /sys
    ```
    /sys/class/net
    /sys/block
    ```
* /opt
    ```
    /opt/google
    /opt/custom_app
    ```
* /mnt /media
    ```
    /mnt        手動掛載
    /media      USB 自動掛載
    ```

## What is .so file?
資料來源: [在Linux中.so和.a檔有什麼差別？](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000P8svSAC&l=zh-TW)
> 副檔名為" .so"的檔案是dynamically linked shared object libraries，簡稱為shared objects、shared libraries或shared object libraries。Shared object libraries在執行時動態載入。Shared object libraries並不是應用程式的一部分，但它們在編譯過程中必須可用取用。一般來說，<span style="background-color: yellow">shared object libraries類似於Windows電腦上的DLL檔</span>。 舉例來說，NI-VISA驅動程式就是使用Shared object libraries。 

## x86、x86_64/x64、amd64和arm64/aarch64
資料來源: [【CPU】關於x86、x86_64/x64、amd64和arm64/aarch64](https://blog.csdn.net/michaelwoshi/article/details/105105421)
> * **x86=i386=IA32**: 是指intel的開發的一種32位指令集，從386開始時代開始的，一直沿用至今，是一種cisc指令集，所有intel早期的cpu，amd早期的cpu都支持這種指令集，intel官方文檔里面稱為“IA-32”
> * **x86_64=x64=AMD64**: 是x86 CPU開始邁向64位的时候
> * **ARM**: （英文為Advanced RISC Machine，或Acorn RISC Machine）也是一個架構，非常適用於移動通信這種低成本，高性能，低耗電的領域。
> **AArch64=ARM64**: 是ARMv8的一種執行狀態。為了更廣泛地向企業領域推進，需要引入 64 位構架，同時也需要在 ARMv8 架構中引入新的 AArch64 執行狀態。AArch64 不是一個單純的 32 位 ARM 構架擴展，而是 ARMv8 內全新的構架，完全使用全新的 A64 指令集。

## Linux 0, 1, 2, 2>&1
資料來源: [Linux 裡的文件描述符 0，1，2， 2＞&1 究竟是什麼](https://blog.csdn.net/yzf279533105/article/details/128587714)
> /dev/null 表示空設備文件
> 0 表示stdin標準輸入
> 1 表示stdout標準輸出
> 2 表示stderr標準錯誤
> * 2>1和2>&1的寫法有什麽區別：
> 2>1的作用是把標準錯誤的輸出重定向到1，但這個1不是標準輸出，而是一個文件!!!,文件名就是1
> 2>&1的作用是把標準錯誤的輸出重定向到標準輸出1，&指示不要把1當作普通文件，而是fd=1即標準輸出來處理。
> * command>a 2>a 與 command>a 2>&1的區別
> 通過上面的分析，對於command>a 2>&1這條命令，等價於command 1>a 2>&1可以理解為執行 command 產生的標準輸入重定向到文件 a 中，標準錯誤也重定向到文件 a 中。那麽是否就說command 1>a 2>&1等價於command 1>a 2>a呢。其實不是，command 1>a 2>&1與command 1>a 2>a還是有區別的，區別就在於前者只打開一次文件a，後者會打開文件兩次，並導致 stdout 被 stderr 覆蓋。&1的含義就可以理解為用標準輸出的引用，引用的就是重定向標準輸出產生打開的 a。從IO效率上來講，command 1>a 2>&1比command 1>a 2>a的效率更高
> * 為何2>&1要寫在後面？
> index.php task testOne >/dev/null 2>&1
> 我們可以理解為，左邊是標準輸出，好，現在標準輸出直接輸入到/dev/null中，而2>&1是將標準錯誤重定向到標準輸出，所以當程序產生錯誤的時候，相當於錯誤流向左邊，而左邊依舊是輸入到/dev/null中。
> 可以理解為，如果寫在中間，那會把隔斷標準輸出指定輸出的文件

## Daemon是什麼
資訊來源: [第十七章、認識系統服務 (daemons)](https://linux.vbird.org/linux_basic/centos7/0560daemons.php)
> 簡單的說，系統為了某些功能必須要提供一些服務 (不論是系統本身還是網路方面)，這個服務就稱為 service 。 但是 service 的提供總是需要程式的運作吧！否則如何執行呢？所以達成這個 service 的程式我們就稱呼他為 daemon 囉！ 舉例來說，達成循環型例行性工作排程服務 (service) 的程式為 crond 這個 daemon 啦！這樣說比較容易理解了吧！

## 要怎麼看netstat
```bash
mark@cctv:~$ netstat -a
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 localhost:8554          0.0.0.0:*               LISTEN
tcp        0      0 localhost:33060         0.0.0.0:*               LISTEN
tcp        0      0 localhost:9081          0.0.0.0:*               LISTEN
tcp        0      0 _localdnsstub:domain    0.0.0.0:*               LISTEN
tcp        0      0 localhost:8888          0.0.0.0:*               LISTEN
tcp        0      0 _localdnsproxy:domain   0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:ssh             0.0.0.0:*               LISTEN
tcp        0      0 localhost:mysql         0.0.0.0:*               LISTEN
tcp        0      0 localhost:7999          0.0.0.0:*               LISTEN
tcp        0      0 localhost:1935          0.0.0.0:*               LISTEN
tcp        0      0 172.18.0.1:37556        172.18.0.2:8554         ESTABLISHED
tcp        0      0 10.129.12.109:ssh       10.10.15.108:36554      ESTABLISHED
tcp        0      1 10.129.12.109:38526     8.8.8.8:domain          SYN_SENT
tcp   107712      0 localhost:50484         localhost:8554          ESTABLISHED
tcp        0 1079838 localhost:8554          localhost:50484         ESTABLISHED
tcp6       0      0 [::]:ssh                [::]:*                  LISTEN
tcp6       0      0 [::]:http               [::]:*                  LISTEN
Active UNIX domain sockets (servers and established)
Proto RefCnt Flags       Type       State         I-Node   Path
unix  3      [ ]         STREAM     CONNECTED     14317    /run/systemd/journal/stdout
unix  3      [ ]         STREAM     CONNECTED     16593
unix  3      [ ]         STREAM     CONNECTED     21307    /run/containerd/containerd.sock.ttrpc
unix  3      [ ]         STREAM     CONNECTED     18538
unix  2      [ ]         DGRAM      CONNECTED     15028
unix  4      [ ]         DGRAM      CONNECTED     9751     /run/systemd/notify
unix  2      [ ACC ]     STREAM     LISTENING     9754     /run/systemd/private
unix  3      [ ]         STREAM     CONNECTED     21321    /run/containerd/containerd.sock.ttrpc
...
```
有分兩個區塊`Internet connections` & `UNIX domain sockets`
* `Internet connections`: host對外的服務，主要看LISTEN這個state，正在等別人連線，ESTABLISHED則是已經建立的連線，Local Address可以看到`[::]:ssh`表示只要外部連線`:20`，就會ssh connection，並且允許任何其他人連線(`[::]:*`)，如果Foreign Address為`0.0.0.0:*`代表這個service只允許這個host本身query
* `UNIX domain sockets`: 這個代表本機內部通訊（process ↔ process）