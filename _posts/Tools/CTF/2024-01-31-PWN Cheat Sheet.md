---
title: PWN Cheat Sheet
tags: [PWN, CTF, Tools]

category: "Tools｜CTF"
date: 2024-01-31
---

# PWN Cheat Sheet
<!-- more -->

## Tools Cheat
* Commonly Used Commands
    ```bash
    $ file {file path}
    $ checksec {file path} # sudo apt-get install checksec
    $ objdump -M intel -d {file path} | less
    $ gdb {file path} # sudo apt-get install gdb
    $ readelf -a {file path} | less # 查看所有資訊，包含section/file-header/program headers/symbol tables/等等
    $ readelf -S {file path} # 只查看sections' header
    $ ldd {file path} # to check what libraries the file used
    ```
* Command Used Tools / Plugin
    * [gdb-peda](https://github.com/longld/peda)
        ```bash
        $ git clone https://github.com/longld/peda.git ~/peda
        $ echo "source ~/peda/peda.py" >> ~/.gdbinit
        ```
    * [radare2](https://github.com/radareorg/radare2)
        ```bash
        $ git clone https://github.com/radare/radare2.git
        $ sudo apt install build-essential # just for wsl
        $ sudo ./radare2/sys/install.sh
        ```
    * [Exploit DB - Shell Code](https://www.exploit-db.com/shellcodes)：如果要寫shell code的話可以直接看exploit db上別人寫好的gadget，複製起來就可以用了，不過有時候也有可能會失敗，在確認其他東西都是正確的情況下，可以試看看別的，記得平台要選對
    * [ROPgadget](https://github.com/JonathanSalwan/ROPgadget)
        ```bash
        $ sudo apt install python3-pip
        $ sudo -H python3 -m pip install ROPgadget
        $ ROPgadget --help
        
        # For using
        $ ROPgadget --binary {executed file} | grep 'pop rax.*ret'
        # Or
        $ ROPgadget --binary {executed file} --only "pop|ret|syscall" > rop_gadget.txt
        $ ROPgadget --binary {executed file} --only "pop|ret|syscall" --multibr > rop_gadget.txt # multibr是multi bransh允許多分支的gadget
        
        # 取得特定string的gadget
        $ ROPgadget --binary {executed file} --string "/bin/sh"
        ```
    * [one_gadget](https://github.com/david942j/one_gadget)
        ```bash
        $ sudo apt install rubygems
        $ sudo gem install one_gadget
        $ one_gadget {libc file}
        ```
    * seccomp-tools
        ```bash
        $ sudo apt install gcc ruby-dev
        $ gem install seccomp-tools
        $ seccomp-tools dump ./test
        ```
    * 找glibc版本的online tool
        * [libc-database search API Search](https://libc.rip/)
        * [libc database search](https://libc.blukat.me/?q=__libc_start_main_ret)

### gdb
常用語法([cheat](https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf))
* b: 設定中斷點
    ```bash
    # break point
    (gdb) b main
    (gdb) b *0x4896aa
    ```
* r: 執行程式 # run `$ (gdb) r`
* c: 繼續執行 # continue `$ (gdb) c`
* si: 步入指令 # step instruction `$(gdb) si`
* ni: 步過指令 # next instruction `$ (gdb) ni`
* x: 顯示記憶體內容
    ```bash
    # show the value stored in memory address
    (gdb) x/10gx 0x400686 # print 10 memory value from 0x400686
    (gdb) x/10gi 0x400686 # print 10 instruction from 0x400686
    (gdb) x/2gs 0x400686 # print 2 strings from 0x400686
    ```
* vmmap 查看address space # check memory permission and distribution `$ (gdb) vmmap`
* bt {number}: 查看call stack
* b info: 查看目前設的break point
* delete breakpoints 1: 刪除一號斷點
* fin: 直接執行該function到結束
* got: 直接查看GOT
* canary: 直接查看canary存放的位置和value
* `heap (chunk|chunks|bins|arenas|set-arena)`
* j/jump {address}: 直接jmp到指定的位置，但要注意如果該位置之後沒有其他breakpoint就會直接執行下去 # jump `$ (gdb) j 0x4896aa`
* set {long}{address} = 0x61616161: 對特定的位址寫入值 # set memory / register value `$ (gdb) set $rax=0x5`
* p &{symbol}: print出特定的symbol
* 如果自己寫一個script讓gdb可以自己load的話可以用: `$ gdb -x {script name} {file name}`
    script範例
    ```
    set LD_PRELOAD=/usr/src/glibc/glibc_dbg/libc.so.6
    b main
    r
    ```
* heapinfo: 查看heap的狀態
* heapb: 就是heap base的command，告訴我們目前的base address
* .gdbinit
    * config
        ```bash
        set disassembly-flavor intel

        define gef
                source ~/.gdbinit-gef.py

                #### gef
                # gef setting
                gef config dereference.max_recursion 2
                gef config context.layout "regs code args source memory stack trace"
                gef config context.nb_lines_backtrace 3
                gef config context.redirect /dev/pts/2
        end
        
        # 以下部分deprecated
        define peda
                #source ~/peda/peda.py
                source ~/Pwngdb/pwngdb.py
                source ~/Pwngdb/angelheap/gdbinit.py

                define hook-run
                python
        import angelheap
        angelheap.init_angelheap()
        end
                end
        end
        ```
    * [pwndbg/pwndbg](https://github.com/pwndbg/pwndbg)
        ```bash
        $ curl --proto '=https' --tlsv1.2 -LsSf 'https://install.pwndbg.re' | sh -s -- -t pwndbg-gdb
        $ pwndbg
        ```

### pwntools
* 常用
    ```python
    raw_input()
    p64(0x401111)
    p32(0x401111)
    r.recvline()
    r.recvuntil(b'test')
    r.recv(6)
    r.sendline(b'test')
    ```
* flat
    ```python
    payload = flat(
        pop_eax_ret, 0,
        pop_ebx_ret, 0xc
    )
    ```
* asm:
    ```python
    payload = asm("""
        xor eax, eax
        xor ebx, ebx
    """)
    ```
* context
    ```python
    context.arch = 'amd64'
    context.newline = b'\r\n' # for windows pe file
    ```
* ELF
    方便查看GOT或function的address
    ```python
    exe = ELF('./vuln')
    log.info("main address: " + hex(exe.symbols['main']))
    log.info("pow GOT address: " + hex(exe.got['pow']))
    log.info("strcspn GOT address: " + hex(exe.got['strcspn']))
    ```
* shellcraft
    pwntools中內建的一些assembly shell code

### Other
* objdump
    ```bash
    $ objdump -M intel -d $binary | less
    ```
* 如果要寫shell code的話可以直接看exploit db上別人寫好的gadget，複製起來就可以用了，不過有時候也有可能會失敗，在確認其他東西都是正確的情況下，可以試看看別的，記得平台要選對
    [Exploit DB - Shell Code](https://www.exploit-db.com/shellcodes)
* [Linux System Call Table](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86-32_bit)
* [Linux System Call Table for x86 64](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)

### 寫/bin/sh\x00的方法
* [Shellcode Cheat Sheet](http://shell-storm.org/shellcode/index.html)
1. 如果是x86版本: 建議直接寫在stack上，因為比較少int 0x80 ; ret的gadget可以用，那倒不如直接寫在script上然後計算esp或ebp的位置，一樣可以拿到儲存的位置
2. 如果是x64版本: 建議可以用system read的方式搭配syscall ret的ROP
3. 如果是直接執行shell code且shell code是可以直接讓我們輸入的話就直接參考exploit db的就好了
* eg 1
    ```
    push 0x0b
    pop eax
    push 0x0068732f
    push 0x6e69622f
    mov ebx, esp
    int 0x80
    ```
* eg 2
    ```
    mov eax, 0x6e69622f
    push eax
    mov eax, 0x0068732f
    push eax
    xor eax, eax
    xor ebx, ebx
    xor ecx, ecx
    xor edx, edx
    mov eax, 0xb
    lea ebx, DWORD PTR [esp]
    int 0x80
    ```
* eg 3
    ```
    /*Put the syscall number of execve in eax*/
        xor eax, eax
        mov al, 0xb
        
        /*Put zero in ecx and edx*/
        xor ecx, ecx
        xor edx, edx
        
        /*Push "/sh\x00" on the stack*/
        xor ebx, ebx
        mov bl, 0x68
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        mov bh, 0x73
        mov bl, 0x2f
        push ebx
        nop
        
        /*Push "/bin" on the stack*/
        mov bh, 0x6e
        mov bl, 0x69
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        shl ebx
        mov bh, 0x62
        mov bl, 0x2f
        push ebx
        nop
                
        /*Move the esp (that points to "/bin/sh\x00") in ebx*/
        mov ebx, esp/*Syscall*/
        int 0x80
    ```

### 如何讓環境執行在指定的libc和loader中
如果不想要費事裝VM或wsl就可以直接用@ccccc提供的腳本，讓這支程式跑在和server一樣的環境，<span style="background-color: yellow">所以要把對應環境的loader和libc載下來</span>，用法如下:
```bash
$ python {script path} {new env loader path} {original elf file}
# e.g. python ./LD_PRELOAD.py ./ld-2.27.so ./vuln
```
他會產生一個新的執行檔，名字是`V`，在pwntools寫的腳本也要改，用法如下
```python
r = process('./V',env={"LD_PRELOAD" : "./libc-2.27.so"})
```

* Script

    ```python
    '''
    Copied and modified from https://www.cnblogs.com/0x636a/p/9157993.html
    All credits ro original author
    '''
    from pwn import *
    import sys, os

    def change_ld(binary, ld):
        """
        Force to use assigned new ld.so by changing the binary
        """
        if not os.access(ld, os.R_OK): 
            log.failure("Invalid path {} to ld".format(ld))
            return None


        if not isinstance(binary, ELF):
            if not os.access(binary, os.R_OK): 
                log.failure("Invalid path {} to binary".format(binary))
                return None
            binary = ELF(binary)


        for segment in binary.segments:
            if segment.header['p_type'] == 'PT_INTERP':
                size = segment.header['p_memsz']
                addr = segment.header['p_paddr']
                data = segment.data()
                if size <= len(ld):
                    log.failure("Failed to change PT_INTERP from {} to {}".format(data, ld))
                    return None
                binary.write(addr, ld.encode().ljust(size, b'\0'))
                path = binary.path.split('/')[-1][0].upper()
                if os.access(path, os.F_OK): 
                    os.remove(path)
                    print("Removing exist file {}".format(path))
                binary.save(path)    
                os.chmod(path, 0b111000000) #rwx------
        print("PT_INTERP has changed from {} to {}. Using temp file {}".format(data, ld, path)) 
        return

    if len(sys.argv)!=3:
        print('Usage : python3 LD_PRELOAD.py [ld] [bin]')
    LD_PATH = sys.argv[1]
    BIN = sys.argv[2]
    change_ld(BIN, LD_PATH)
    ###Execute file by 'LD_PRELOAD={target_libc} ./executable'
    ```

* How to download libc file & loader
    * [Ubuntu Packages Search](https://packages.ubuntu.com/)
    * [libc6_2.31-0ubuntu9_amd64.deb](https://ubuntu.pkgs.org/20.04/ubuntu-main-amd64/libc6_2.31-0ubuntu9_amd64.deb.html)

## Stack Vulnerabilities
### `checksec`
* No RELRO or Partial RELRO → <span style="background-color: yellow">GOT Hijacking(改寫GOT)</span>
    * No RELRO - link map和GOT都可寫(有lazy binding)
    * Partial RELRO - link map不可寫，GOT可寫(有lazy binding)
    * Full RELRO - link map和GOT都不可寫(事先把library的位置都先resolve完並寫在GOT上，再把GOT權限關掉，比較花時間但安全)
    * 關閉指令：`-z norelro`
* Position Independent Executable(PIE) → <span style="background-color: yellow">BOF(ret2 series)</span>
    * 開啟時，data 段以及 code 段位址隨機化
    * 關閉時，data 段以及 code 段位址固定
    * 關閉指令：`-no-pie`
* NX (No eXecute, Data Execution Prevention, DEP) off → 基本上不能直接執行shellcode，但可以用<span style="background-color: yellow">ROP</span>繞過
    * 可寫得不可執⾏，可執⾏的不可寫
    * 關閉指令：`-zexecstack`
* ASLR (Address Space Layout Randomization)
    * 記憶體位址隨機變化
    * 每次執⾏時，stack、heap、library 位置都不⼀樣
    * 關閉指令: `sudo sh -c "echo 0 > /proc/sys/kernel/randomize_va_space"`
    * 打開指令: `sudo sh -c "echo 2 > /proc/sys/kernel/randomize_va_space"`
* Stack Canary
    * 關閉指令：`-fno-stack-protector`

### Bof Series
* Overwrite sensitive data
* Overwrite return address -> 
    * Statically Link Binary: 可以直接試看看ROP chain(從binary本身找gadget)
    * Dynamically Link Binary: 看有沒有辦法leak出libc base address，再用ROP chain(從libc中找gadget)
* Canary
    * Leak canary
* 如果BoF的長度不夠的話，可以考慮用stack pivot的方式再搭配ROP chain: 範例可以參考[Lab - Stack Pivot](https://hackmd.io/@SBK6401/SkpDfz4BT)

### Format String Bug
* 之前的Demo是利用format string達到<span style="background-color: yellow">GOT hijack</span>
* 用法:
    * %**p** - leak code / libc / stack address
    * %{**任意值**}c%**k**$(hhn\|hn\|n) - 寫**任意值**到第 **k** 個參數指向的位址
    * %**X**c - 印出 **X** 個字元
    * **k**$ - 指定第 **k** 個參數
    * %(hhn\|hn\|n) - 將**輸出的字元數**以 1 / 2 / 4 bytes 寫到參數**指向的位址**
    * 若該值為 addr 可透過 %s 輸出該地址的 value
* Note:
    * 因為能控制寫入的⼤⼩與位址，因此也可以配合 partial overwrite 做 exploit
    * 基本上不太會⽤ %k$n 此 format，因為⼀次寫入 4 bytes 會太多

### GOT Series
* GOT hijacking
* Ret2plt - 控制執⾏流程到 function@plt，也代表執⾏該 function (以 functionA 代稱)，詳細可以看[0x32 Ret2Plt](https://hackmd.io/@SBK6401/SyAHQfQH6)
* Leak libc - functionA 在被解析後，GOT 會存放 functionA 的絕對位址，因此如果可以讀取 GOT，就能得到位於 library 當中的 address
    * FunctionA 的絕對位址減去他在 library 當中的 offset，能得到 library base address，繞過 ASLR
* Ret2libc - 有了 library base address，也能加上其他 function 的 offset 來取得該
    * function 在 library 中的位址 (以 functionB 代稱)藉由控制程式流程，讓程式跳到 functionB 上，意即執⾏此 functionB

### Return 2 Series
1. Return 2 Code(**必要條件：PIE Off**): 這是代表原本的source code就已經有寫好一個shell，只要改變RIP就可以跳過去
2. Return 2 Shell Code(**必要條件：NX Off(要完全可讀可寫可執行)**): 代表我們要自己寫一個shell code在記憶體中，然後用RIP跳過去
    * 作法就是先找到一塊rwx全開的地方，然後想辦法把shell code寫上去，接著控制RIP跳到該段拿到shell
    * 變形：就像[^pico_pwn_guessing_game_1]和[^ntucs_pwn_rop++]一樣，可以先找到.bss section，然後開__libc_read function寫入`/bin/sh\x00`，之後再return到shell code的地方
3. Return 2 libc

## Heap Vulnerabilities
### Background
* 解題關鍵
* ![圖片](https://hackmd.io/_uploads/ByQ16zsrT.png)
* ![圖片](https://hackmd.io/_uploads/ByCZaGiHa.png)
* ![圖片](https://hackmd.io/_uploads/HkFM6MjHp.png)
* ![圖片](https://hackmd.io/_uploads/rkUXpMoB6.png)

### Double Free
### Used After Free
* [UAF leak Libc address](https://hackmd.io/@SBK6401/SJWc9v4Bp#%E5%A6%82%E4%BD%95%E7%94%A8UAF-leak-libc-address)
* [UAF leak heap address](https://hackmd.io/@SBK6401/SJWc9v4Bp#%E5%A6%82%E4%BD%95%E7%94%A8UAF-leak-heap-address)
* 基本的練習可以看[UAF++](https://hackmd.io/@SBK6401/SyXdjA5r6)

### Tcache poisoning
使⽤ double free 讓 tcache 當中存在兩個相同的 chunk，並利⽤修改 fd的⽅式，將對應位址視為 chunk 分配給 user
* Tcache 拿 chunk 時並不會檢查 chunk size 是否合法，因此常會拿 __free_hook 寫 system
* Protection 1 - 當釋放 chunk 時，如果 chunk + 8 (key) 位置的值與當前 heap 的&tcache_struct 相等，則會遍歷所有 entry，檢查是否有相同的 chunk，確保沒有double free 的發⽣
* Protection 2 - 當取出 chunk 時，會檢查對應⼤⼩的 counter 是否⼤於 0，如果是的話才會取出 tcache_struct 當中指向的第⼀塊 chunk
* Bypass Protection 1 - 透過 UAF 或是 heap overflow，修改 chunk 的 key 欄位
* Bypass Protection 2
    * 拿到 tcache_struct 的 chunk 後修改 counts 欄位成非 0 的值
    * 多次 free 相同的 chunk

### Overlapping chunks
簡單來說就是<span style="background-color: yellow">修改chunk size</span>，讓 chunk 在被釋放時 trigger consolidation(當釋放記憶體時，若檢查到相鄰的 chunk 沒有被使⽤，會將其合併成⼀塊更⼤的 freed chunk)，使得正在使⽤的 chunk 與已經釋放的 chunk 有部分重疊，也就代表
* 使⽤中的 chunk 可以更改 freed chunk 中的 fd、bk
* freed chunk 在被分配時，會分配到與使⽤中的 chunk 相同的區塊，可以修改敏感資料

## Reference
[^pico_pwn_guessing_game_1]:[Guessing Game 1](https://hackmd.io/@SBK6401/SkxoLuwoh)
[^ntucs_pwn_rop++]:[Simple PWN - 0x12(Lab - rop++)](https://hackmd.io/@SBK6401/rysBjQfjs)