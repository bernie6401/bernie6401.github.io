---
title: Linux Related
tags: [名詞解釋]

---

* What is .so file?
    資料來源: [在Linux中.so和.a檔有什麼差別？](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000P8svSAC&l=zh-TW)
    > 副檔名為“ .so”的檔案是dynamically linked shared object libraries，簡稱為shared objects、shared libraries或shared object libraries。Shared object libraries在執行時動態載入。Shared object libraries並不是應用程式的一部分，但它們在編譯過程中必須可用取用。一般來說，shared object libraries類似於Windows電腦上的DLL檔。 舉例來說，NI-VISA驅動程式就是使用Shared object libraries。 

* x86、x86_64/x64、amd64和arm64/aarch64
    資料來源: [【CPU】關於x86、x86_64/x64、amd64和arm64/aarch64](https://blog.csdn.net/michaelwoshi/article/details/105105421)
    > * ==**x86=i386=IA32**==: 是指intel的開發的一種32位指令集，從386開始時代開始的，一直沿用至今，是一種cisc指令集，所有intel早期的cpu，amd早期的cpu都支持這種指令集，intel官方文檔里面稱為“IA-32”
    > * ==**x86_64=x64=AMD64**==: 是x86 CPU開始邁向64位的时候
    > * ==**ARM**==: （英文為Advanced RISC Machine，或Acorn RISC Machine）也是一個架構，非常適用於移動通信這種低成本，高性能，低耗電的領域。
    > ==**AArch64=ARM64**==: 是ARMv8的一種執行狀態。為了更廣泛地向企業領域推進，需要引入 64 位構架，同時也需要在 ARMv8 架構中引入新的 AArch64 執行狀態。AArch64 不是一個單純的 32 位 ARM 構架擴展，而是 ARMv8 內全新的構架，完全使用全新的 A64 指令集。

* Linux 0, 1, 2, 2>&1
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