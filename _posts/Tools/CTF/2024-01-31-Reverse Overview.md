---
title: Reverse Overview
tags: [CTF, Reverse, Tools]

category: "Tools｜CTF"
date: 2024-01-31
---

# Reverse Overview
<!-- more -->

## Tools

| Type| App| .NET| x86/x64| Packer| Python| C|General|
| - | - | - | - | - | - | - | - |
| Description | <li> MobSF: Must run in python `3.8`</li><li>ApkTool: Just follow the step in [install guide](https://apktool.org/docs/install/)</li>|To decompile C#(.NET)|| 指令：`$ upx -d {filename}`|| 一個可以把組語轉換成c pseudo code的線上工具 |一個線上的decompiler，結合多種工具，只要上傳檔案(小於2MB)就可以呈現多種decompiler tools的結果|
| Link| [MobSF](https://ithelp.ithome.com.tw/articles/10215522)</br>[ApkTools](https://apktool.org/) | [dnSpy](https://github.com/dnSpy/dnSpy/releases) | [x86模擬器](https://carlosrafaelgn.com.br/Asm86/)</br>[x86/x64 assembler/disassembler](https://defuse.ca/online-x86-assembler.htm#disassembly) | [UPX Packer](https://github.com/upx/upx/releases/tag/v4.0.2) | [Pyc disassemble](https://tool.lu/pyc/) | [Compiler Explorer](https://godbolt.org/)   |[Decompiler Explorer](https://dogbolt.org/)|

## IDA 常用快捷鍵
* [IDA Interface](https://blog.30cm.tw/2018/01/ida.html)
* 型別
    * char(1 byte)
    * WORD(2 bytes)
    * DWORD(4 bytes)
    * PDWORD(pointer of DWORD = DWORD \*)
    * 若是DWORD \*name，代表name這個變數是一個pointer而且指向的地方是一個DWORD
* Space: 在 Text View / Graph View 切換
* Tab: 在視窗之間切換
* ;/Insert: 註解
* x: 秀出 Xrefs
* n: 改名 
* y: 改型別
* h: 改表示方式 (dec / hex)
* u: 取消定義
* a: 當成字串
* c: 當成code
* p: 當成function
* t: set sizeof(XXX)；如果已經確定目前的constant就是某個變數的length，那可以直接按t讓他變成sizeof(那個變數)
    舉例：如果已經確定目前的`0x238`就是`PROCESSENTRY32W`的size，就可以直接這樣用，會變得比較清楚
    * 結果
        ![](https://hackmd.io/_uploads/S1nruHTza.png)
        ![](https://hackmd.io/_uploads/rkjwuBTza.png)
* Shift+F1: show出Local Type視窗
    * Local Types Screenshot
        ![](https://hackmd.io/_uploads/S1ikDa5_n.png)*
* Shift+F12: 開啟Strings視窗
    * Strings Screenshot
        ![](https://hackmd.io/_uploads/HybvLzo_2.png)*
* 對某一個數值按m: ENUM這個功能就是在替換一些常見的windows API參數，讓原本的純數字可以用文字表示，這樣比較好懂API的操作，逆向會更順暢(補充說明：IDA有收錄很多MSDN上的一些API，他每一個參數表示的文字，例如[這一篇](https://learn.microsoft.com/en-us/windows/win32/Memory/memory-protection-constants)底下有顯示很多Constant/value的對應，而正常情況下IDA會顯示的是value，如果要把它換成Constant文字的表達式就可以用到ENUM這個功能)，又例如:
    目前已經知道`CreateToolhelp32Snapshot(2, 0);`中的2的意義是`TH32CS_SNAPPROCESS`(可以參考[MSDN](https://learn.microsoft.com/zh-tw/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot#parameters))，此時就可以直接按m之後再選擇`TH32CS_SNAPPROCESS`
    *
    ![](https://hackmd.io/_uploads/B1Rn5Q6G6.png)*
* \\: 不顯示/顯示資料型別
* Alt+M/Ctrl+M: 前者是註冊書籤，後者是察看並選擇標籤，可以快速跑到標示的地址
* Ctrl+E: 如果是分析DLL file，可能會有很多不同的entry point，利用這個shortcut可以顯示目前有幾個entry point，很方便
    ![](https://hackmd.io/_uploads/ryJw-C6Ga.png)*
* 如何把bytes變成字串: 
    * 可以直接Alt+A
        1. 可以先把bytes的型別定義好(單獨的bytes變成array)，變成array有兩種方法，第一種是直接用`Y`定義他的型別成`int dword_2008[32]`，前面的int就看每一個字元是來決定，後面`[32]`就代表有多少字元變成array；第二種方法就是直接按`d`改變一個字元的型態變成int，然後在`edit/Array`的地方可以叫出`Convert to array`的視窗(如果前面沒有先用`d`改變型態的話，他會以為所有字元都是一個byte，然後總共有128個字元這樣換算，但其實我們是總共32個字元，每一個字元是4個bytes，也就是int，這一點要特別注意)
            ![](https://hackmd.io/_uploads/HJ3yvI-Ga.png)
            ![](https://hackmd.io/_uploads/r1A_8LWMa.png)
        2. 接著就是在`Option/String literals`視窗中設定用哪一個型態表示字串，這邊因為每一個字元都是4 bytes，也就是32 bits，所以選擇C-style
            ![](https://hackmd.io/_uploads/SyQBP8Zfp.png)*
    * 完整流程
    ```
    .rodata:0000000000002008 unk_2008 db  46h ; F                    ; DATA XREF: main+8↑o
    .rodata:0000000000002009 db    0
    .rodata:000000000000200A db    0
    .rodata:000000000000200B db    0
    .rodata:000000000000200C db  4Ch ; L
    .rodata:000000000000200D db    0
    .rodata:000000000000200E db    0
    .rodata:000000000000200F db    0
    .rodata:0000000000002010 db  41h ; A
    .rodata:0000000000002011 db    0
    .rodata:0000000000002012 db    0
    .rodata:0000000000002013 db    0
    .rodata:0000000000002014 db  47h ; G
    .rodata:0000000000002015 db    0
    .rodata:0000000000002016 db    0
    .rodata:0000000000002017 db    0
    .rodata:0000000000002018 db  7Bh ; {
    .rodata:0000000000002019 db    0
    .rodata:000000000000201A db    0
    .rodata:000000000000201B db    0
    .rodata:000000000000201C db  68h ; h
    .rodata:000000000000201D db    0
    .rodata:000000000000201E db    0
    .rodata:000000000000201F db    0
    .rodata:0000000000002020 db  33h ; 3
    .rodata:0000000000002021 db    0
    .rodata:0000000000002022 db    0
    .rodata:0000000000002023 db    0
    .rodata:0000000000002024 db  31h ; 1
    .rodata:0000000000002025 db    0
    .rodata:0000000000002026 db    0
    .rodata:0000000000002027 db    0
    .rodata:0000000000002028 db  31h ; 1
    .rodata:0000000000002029 db    0
    .rodata:000000000000202A db    0
    .rodata:000000000000202B db    0
    .rodata:000000000000202C db  4Fh ; O
    .rodata:000000000000202D db    0
    .rodata:000000000000202E db    0
    .rodata:000000000000202F db    0
    .rodata:0000000000002030 db  5Fh ; _
    .rodata:0000000000002031 db    0
    .rodata:0000000000002032 db    0
    .rodata:0000000000002033 db    0
    .rodata:0000000000002034 db  72h ; r
    .rodata:0000000000002035 db    0
    .rodata:0000000000002036 db    0
    .rodata:0000000000002037 db    0
    .rodata:0000000000002038 db  65h ; e
    .rodata:0000000000002039 db    0
    .rodata:000000000000203A db    0
    .rodata:000000000000203B db    0
    .rodata:000000000000203C db  76h ; v
    .rodata:000000000000203D db    0
    .rodata:000000000000203E db    0
    .rodata:000000000000203F db    0
    .rodata:0000000000002040 db  65h ; e
    .rodata:0000000000002041 db    0
    .rodata:0000000000002042 db    0
    .rodata:0000000000002043 db    0
    .rodata:0000000000002044 db  72h ; r
    .rodata:0000000000002045 db    0
    .rodata:0000000000002046 db    0
    .rodata:0000000000002047 db    0
    .rodata:0000000000002048 db  73h ; s
    .rodata:0000000000002049 db    0
    .rodata:000000000000204A db    0
    .rodata:000000000000204B db    0
    .rodata:000000000000204C db  31h ; 1
    .rodata:000000000000204D db    0
    .rodata:000000000000204E db    0
    .rodata:000000000000204F db    0
    .rodata:0000000000002050 db  6Eh ; n
    .rodata:0000000000002051 db    0
    .rodata:0000000000002052 db    0
    .rodata:0000000000002053 db    0
    .rodata:0000000000002054 db  67h ; g
    .rodata:0000000000002055 db    0
    .rodata:0000000000002056 db    0
    .rodata:0000000000002057 db    0
    .rodata:0000000000002058 db  5Fh ; _
    .rodata:0000000000002059 db    0
    .rodata:000000000000205A db    0
    .rodata:000000000000205B db    0
    .rodata:000000000000205C db  33h ; 3
    .rodata:000000000000205D db    0
    .rodata:000000000000205E db    0
    .rodata:000000000000205F db    0
    .rodata:0000000000002060 db  6Eh ; n
    .rodata:0000000000002061 db    0
    .rodata:0000000000002062 db    0
    .rodata:0000000000002063 db    0
    .rodata:0000000000002064 db  67h ; g
    .rodata:0000000000002065 db    0
    .rodata:0000000000002066 db    0
    .rodata:0000000000002067 db    0
    .rodata:0000000000002068 db  69h ; i
    .rodata:0000000000002069 db    0
    .rodata:000000000000206A db    0
    .rodata:000000000000206B db    0
    .rodata:000000000000206C db  6Eh ; n
    .rodata:000000000000206D db    0
    .rodata:000000000000206E db    0
    .rodata:000000000000206F db    0
    .rodata:0000000000002070 db  65h ; e
    .rodata:0000000000002071 db    0
    .rodata:0000000000002072 db    0
    .rodata:0000000000002073 db    0
    .rodata:0000000000002074 db  65h ; e
    .rodata:0000000000002075 db    0
    .rodata:0000000000002076 db    0
    .rodata:0000000000002077 db    0
    .rodata:0000000000002078 db  72h ; r
    .rodata:0000000000002079 db    0
    .rodata:000000000000207A db    0
    .rodata:000000000000207B db    0
    .rodata:000000000000207C db  35h ; 5
    .rodata:000000000000207D db    0
    .rodata:000000000000207E db    0
    .rodata:000000000000207F db    0
    .rodata:0000000000002080 db  7Dh ; }
    .rodata:0000000000002081 db    0
    .rodata:0000000000002082 db    0
    .rodata:0000000000002083 db    0
    .rodata:0000000000002084 db    0
    .rodata:0000000000002085 db    0
    .rodata:0000000000002086 db    0
    .rodata:0000000000002087 db    0
    ```
    $\downarrow$
    ```
    .rodata:0000000000002008 dword_2008 dd 46h, 4Ch, 41h, 47h, 7Bh, 68h, 33h, 2 dup(31h), 4Fh, 5Fh, 72h, 65h, 76h, 65h, 72h, 73h, 31h, 6Eh, 67h
    .rodata:0000000000002008                                         ; DATA XREF: main+8↑o
    .rodata:0000000000002008 dd 5Fh, 33h, 6Eh, 67h, 69h, 6Eh, 2 dup(65h), 72h, 35h, 7Dh, 0
    ```
    $\downarrow$
    ```
    .rodata:0000000000002008 text "UTF-32LE", 'FLAG{h311O_revers1ng_3ngineer5}',0
    ```
* 如何快速把bytes dump出來
    1. 選擇要輸出的bytes
        ![](https://hackmd.io/_uploads/Syc9UkTM6.png)
    2. 按Shift+E，跳出的視窗選擇想要的格式，再直接複製即可
        ![](https://hackmd.io/_uploads/SJ7a8ypfT.png)
* 如果函式沒有return東西的話，可以右鍵該函示，選擇`Remove return value`或是Shift+Del
    ![](https://hackmd.io/_uploads/HkRk3JpG6.png)
* 如果function中的宣告很多，可以右鍵選擇`Collapse declarations`
    ![](https://hackmd.io/_uploads/SkOXU4AMa.png)

## x64dbg 常用快捷鍵
* F2: 設定中斷點
* F9: 繼續執行
* F8: 步過
* F7: 步入
* Ctrl+F9: 執行到 ret
* ==Ctrl+G==: goto
* ==Space==: 修改組譯

### 靜態分析
* PEview
* PEViewer
* PE-bear

### 動態分析
* OllyDbg
* x64dbg
* IDA
* Ghidra
* Windbg
* PEtool

### Process相關的操作與資訊
* Procexp & Process Hacker
    好看版的工作管理員
* Procmon
    監控程序行為
    Registry
    File system
    Network
    Process/Thread

### 好用的解題工具
* [angr - cheatsheet](https://docs.angr.io/en/latest/appendix/cheatsheet.html): `$ pip install angr claripy`
* z3: `$ pip install z3-solver`