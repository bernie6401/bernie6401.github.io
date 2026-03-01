---
title: Reverse Cheat Sheet
tags: [CTF, Reverse, Tools]

category: "Tools｜CTF"
date: 2024-01-31
---

# Reverse Cheat Sheet
<!-- more -->

## 解題思路
1. 先觀察
    ```bash
    $ file <file>
    ```

## Tools

|**Type**| Description| Link|
| ----------- | --- | --- |
| **App**     | MobSF: Must run in python `3.8`<br>ApkTool: Just follow the step in install guide | [MobSF](https://ithelp.ithome.com.tw/articles/10215522)<br>[ApkTools](https://apktool.org/)|
| **.NET**    | To decompile C#(.NET)| [dnSpy](https://github.com/dnSpy/dnSpy/releases)|
| **x86/x64 Simulator** || [x86模擬器](https://carlosrafaelgn.com.br/Asm86/)<br>[x86/x64 assembler/disassembler](https://defuse.ca/online-x86-assembler.htm#disassembly) |
| **Python**  || [Pyc disassemble](https://tool.lu/pyc/)|
| **asm→C**       | 一個可以把組語轉換成 c pseudo code 的線上工具| [Compiler Explorer](https://godbolt.org/)|
| **General** | 一個線上的 decompiler，結合多種工具，只要上傳檔案 (小於2MB) 就可以呈現多種 decompiler tools 的結果| [Decompiler Explorer](https://dogbolt.org/)|

## IDA 常用快捷鍵
* [IDA Interface](https://blog.30cm.tw/2018/01/ida.html)
* 型別
    * char(1 byte)
    * WORD(2 bytes)
    * DWORD(4 bytes)
    * PDWORD(pointer of DWORD = DWORD \*)
    * 若是DWORD \*name，代表name這個變數是一個pointer而且指向的地方是一個DWORD
* 關閉Opcode: 有時候會不想要看哪麼多Opcoder就可以使用，`Options/General → Number of opcode bytes (non-graph)`設定成 0
* Decompile: `F5`
* Space: 在 Text View / Graph View 切換
* Tab: 在視窗之間切換
* ;/Insert: 註解
* x: 秀出 Xrefs
* n: 改名 
* y: 改型別
* h: 改表示方式 (dec / hex)
* u: 取消定義，可以框選起來做操作
* a: 當成字串，可以框選起來做操作
* c: 當成code，可以框選起來做操作，將 IDA 認不出來的部分當成 Code
* p: 當成function，可以框選起來做操作，通常是將紅色區域標成 Function
* t: set sizeof(XXX)；如果已經確定目前的constant就是某個變數的length，那可以直接按t讓他變成sizeof(那個變數)
    舉例：如果已經確定目前的`0x238`就是`PROCESSENTRY32W`的size，就可以直接這樣用，會變得比較清楚
    ![](https://hackmd.io/_uploads/S1nruHTza.png)
    ![](https://hackmd.io/_uploads/rkjwuBTza.png)
* Shift+F1: show出Local Type視窗
    ![](https://hackmd.io/_uploads/S1ikDa5_n.png)
* Shift+F12: 開啟Strings視窗
    ![](https://hackmd.io/_uploads/HybvLzo_2.png)
* 對某一個數值按m: ENUM這個功能就是在替換一些常見的windows API參數，讓原本的純數字可以用文字表示，這樣比較好懂API的操作，逆向會更順暢(補充說明：IDA有收錄很多MSDN上的一些API，他每一個參數表示的文字，例如[這一篇](https://learn.microsoft.com/en-us/windows/win32/Memory/memory-protection-constants)底下有顯示很多Constant/value的對應，而正常情況下IDA會顯示的是value，如果要把它換成Constant文字的表達式就可以用到ENUM這個功能)，又例如:
    目前已經知道`CreateToolhelp32Snapshot(2, 0);`中的2的意義是`TH32CS_SNAPPROCESS`(可以參考[MSDN](https://learn.microsoft.com/zh-tw/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot#parameters))，此時就可以直接按m之後再選擇`TH32CS_SNAPPROCESS`
    ![](https://hackmd.io/_uploads/B1Rn5Q6G6.png)*
* \\: 不顯示/顯示資料型別
* Alt+M/Ctrl+M: 前者是註冊書籤，後者是察看並選擇標籤，可以快速跑到標示的地址
* Ctrl+E: 如果是分析DLL file，可能會有很多不同的entry point，利用這個shortcut可以顯示目前有幾個entry point，很方便
    ![](https://hackmd.io/_uploads/ryJw-C6Ga.png)
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
    ↓
    ```
    .rodata:0000000000002008 dword_2008 dd 46h, 4Ch, 41h, 47h, 7Bh, 68h, 33h, 2 dup(31h), 4Fh, 5Fh, 72h, 65h, 76h, 65h, 72h, 73h, 31h, 6Eh, 67h
    .rodata:0000000000002008                                         ; DATA XREF: main+8↑o
    .rodata:0000000000002008 dd 5Fh, 33h, 6Eh, 67h, 69h, 6Eh, 2 dup(65h), 72h, 35h, 7Dh, 0
    ```
    ↓
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
* Ctrl+G: goto
* Space: 修改組譯

## 靜態分析
* PEview
* PEViewer
* PE-bear

## 動態分析
* OllyDbg
* x64dbg
* IDA
* Ghidra
* Windbg
* PEtool

## Process相關的操作與資訊
* Procexp & Process Hacker
    好看版的工作管理員
* Procmon
    * 監控程序行為
    * Registry
    * File system
    * Network
    * Process/Thread

## 好用的解題工具
* [angr - cheatsheet](https://docs.angr.io/en/latest/appendix/cheatsheet.html): `$ pip install angr claripy`
    
    直接對 binary 做 symbolic execution 幫你「走所有路徑」找出能到 win() 的 input

    適合在：
    * 很多巢狀 if statement
    * 很多跳轉或是複雜的Control Flow Graph或是switch
    * 很多驗證流程

    angr基本流程 - 範例來自 [Simple-Reverse-0x28(2023-Lab-Super-Angry)/]({{base.url}}/Simple-Reverse-0x28(2023-Lab-Super-Angry)/)
    * 建立一個project: `import angr; import claripy; proj = angr.Project('./super_angry')`
    * 建立claripy symbol - 以這個lab的例子來說就是建立我們輸入進去的程式的input string
        ```python
        sym_arg = claripy.BVS('sym_arg', 8 * 32) # 就像z3一樣要建立symbol
        ```
    * 建立初始的state - 以這個lab來說就是我們一開始輸入的input string
        ```python
        state = proj.factory.entry_state(args=[proj.filename, sym_arg])
        simgr = proj.factory.simulation_manager(state)
        ```
    * 有了proj / symbol / initial state之後就要開始讓他跑起來
        ```python
        simgr.explore(find = lambda s: b'Correct!' in  s.posix.dumps(1))
        ```

* z3: `$ pip install z3-solver`

    適合解：
    * 複雜條件判斷
    * bitwise 運算
    * 多個 if 組合
    * 需要算出滿足條件的輸入

    z3的大致步驟 - 範例來自 [Simple-Reverse-0x27(2023-Lab-Scramble)/]({{base.url}}/Simple-Reverse-0x27(2023-Lab-Scramble)/)
    * 建立一個solver: `from z3 import *; s = Solver()`
    * 建立符號 - 以此lab來說就是建立43個符號對應每一個flag字元: `bvs = [BitVec(f'bt_{i}', 32) for i in range(flag_len)]`
    * 加上constraint - 以此lab來說每一個flag字元都應該限制在空白到0x7f之間，另外還要加上每一個符號(就是flag字元)，經過我們已知的scramble pattern之後應該要是最後的target: 
        ```python
        for bv in bvs:
            s.add(And(bv >= 0x20, bv <= 0x7f))
        for i, patter in enumerate(patters):
            formula = f'bvs[{i}]'

            for step in patter:
                op = step[0]
                value = step[1]

                if op == 'add':
                    formula = f'({formula} + {value})'
                elif op == 'sub':
                    formula = f'({formula} - {value})'
                elif op == 'lsh':
                    formula = f'({formula} << {value})'

            print(f'{formula} == {targets[i]}')
            s.add(eval(formula) == targets[i])    
        ```
    * 判斷有無解，如果有的話就把每一個符號的值取出來
        ```python
        if s.check() == sat:
            print('Find ~~~')
            print(s.model())

            flag = ""
            for bv in bvs:
                flag += chr(s.model()[bv].as_long())

            print(flag)
        ```
    
## Anti-Revese
* Scylla Hide
### Anti-Debug
* 比較時間差，在程式的各種地方插入檢查時間與製造 Delay
* Win32 API
    * IsDebuggerPresent()
    * CheckRemoteDebuggerPresent()
    * RtlQueryProcessHeapInformation()
    * RtlQueryProcessDebugInformation()
    * NtQuerySystemInformation()
    * NtQueryInformationProcess(): 這個 API 可以 Query 很多種類的 Process Information，更詳細的就看講義
#### 比較時間差解法
* 做 Patch 直接把 Timer, Sleep 相關的東西全都 NOP 掉
* Hook 時間函數做 Speed Hack 讓時間變快
    * 可以用 CheatEngine 做 SpeedHack
    * 但要注意 Debugger 不能共存這件事情
#### Win32 API解法
Hook 掉這些 Function 就好，讓回傳值跟沒被 Debug 的數值一樣，但隨便 Hook 也會有機會被發現

### Anti-Disassembler: 讓 Disassembler 壞掉的小技巧
* 針對線性掃描: 因為指令集密度很高，如果在程式中製造 Offset…，可能會解出看起來對的程式碼，但行為可能根本不一樣
* 針對 Control-flow Based Disassembler: 因為這種 Disassembler 會根據 Control-Flow 做追蹤，如果利用假的 jmp 指令來跳躍，可以使分析頭跳到奇怪的地方，然後就解壞了
#### 解法
* 把解析壞掉的部分 Undefine 掉，找到對的 Code 開始點再標記回去，就是 IDA 的`u`,`c`的功能應用

### Anti-Attach: 在 Windows 下，ntdll 有一個函數可以用來做到 Anti-Attach → **DbgUiRemoteBreakin**
### Packing
* 加密殼: Themida, VMProtect, ASProtect
* 壓縮殼: UPX, ASPack
    * [UPX Packer](https://github.com/upx/upx/releases/tag/v4.0.2)
        ```bash
        $ upx -d {filename}`
        ```
* VM殼: 將程式變成另外一種客製化的 Bytecode 並跑在 VM 裡面，e.g. VMProtect, Themida

#### 脫殼方式
1. 找工具
2. 如果看懂殼的邏輯就手動脫殼
3. 動態脫殼：等動態跑起來後，程式邏輯被解密就直接dump memory

### Obfuscation
* 通過 Obfuscator 將程式碼扭成麻花，e.g. 編譯器優化
* 參雜垃圾 Code
* 在 Control-Flow Graph 上面畫畫的 REPsych, Artfuscator
* 把 Control-Flow 變成一直線的 Movfuscator
* 將 if 這種 branch 攤平 → 用一個 loop 加 switch 來做分支攤平
* 將程式碼小片段變成某種 State Machine
* 一些將程式碼片段搞消失的方法
* 通過各種加載手段來映射片段的程式碼 → VirtualAlloc, VirtualProtect, mmap, mprotect
* 把程式切成小份到處亂丟，要用的時候再解包出來 map 到記憶體上