---
title: Simple Reverse - 0x14(2023 Lab - AssemblyDev)
tags: [eductf, CTF, Reverse]

category: "Security/Course/NTU CS/Reverse"
---

# Simple Reverse - 0x14(2023 Lab - AssemblyDev)
## Background
Tools
[Assembly x86 Emulator](https://carlosrafaelgn.com.br/Asm86/)
[Compiler Explorer](https://godbolt.org/)
## Source code
:::spoiler arithmatic.py
```python
#!/usr/bin/python
from module.checker import *
from module.math import *
from sys import argv

challenge_info = f'''
let a = MEM[RSP+0x0:RSP+0x4]
let b = MEM[RSP+0x4:RSP+0x8]
let c = MEM[RSP+0x8:RSP+0xc]

EAX = a + b
EBX = a - b
ECX = -c
EDX = 9*a + 7
'''

a = get_rand(4)
b = get_rand(4)
c = get_rand(4)

init_list = [
    (RSP_DEFAULT + 0x0, a, 4),
    (RSP_DEFAULT + 0x4, b, 4),
    (RSP_DEFAULT + 0x8, c, 4),
]
ans_list = [
    ("eax", add(a, b, 4)),
    ("ebx", sub(a, b, 4)),
    ("ecx", neg(c, 4)),
    ("edx", add(mul(a, 9, 4), 7, 4)),
]

if __name__ == "__main__":
    if len(argv) < 2:
        print(f"{C.BLUE}[+]{C.NC} Usage: python3 {__file__} <path_to_asm_file>")
        print(challenge_info)
        exit(0)

    code = open(argv[1], 'r').read()
    Checker(init_list, ans_list, code)

```
:::
:::spoiler data_movement.py
```python
#!/usr/bin/python
from module.checker import *
from module.math import *
from sys import argv

challenge_info = f'''
{C.BLUE}# Modify register value{C.NC}
RAX += 0x87
RBX -= 0x63
RCX, RDX = RDX, RCX

{C.BLUE}# Modify memory value{C.NC}
MEM[RSP+0x0:RSP+0x4] += 0xdeadbeef
MEM[RSP+0x4:RSP+0x8] -= 0xfaceb00c
MEM[RSP+0x8:RSP+0xc], MEM[RSP+0xc:RSP+0x10] = MEM[RSP+0xc:RSP+0x10], MEM[RSP+0x8:RSP+0xc]
'''

_rax = get_rand()
_rbx = get_rand()
_rcx = get_rand()
_rdx = get_rand()
mem = list()
for i in range(4):
    mem.append(get_rand(4))

init_list = [
    ("rax", _rax),
    ("rbx", _rbx),
    ("rcx", _rcx),
    ("rdx", _rdx),
    (RSP_DEFAULT + 0x0, mem[0], 4),
    (RSP_DEFAULT + 0x4, mem[1], 4),
    (RSP_DEFAULT + 0x8, mem[2], 4),
    (RSP_DEFAULT + 0xc, mem[3], 4),
]
ans_list = [
    ("rax", add(_rax, 0x87)),
    ("rbx", sub(_rbx, 0x63)),
    ("rcx", _rdx),
    ("rdx", _rcx),
    (RSP_DEFAULT + 0x0, add(mem[0], 0xdeadbeef, 4), 4),
    (RSP_DEFAULT + 0x4, sub(mem[1], 0xfaceb00c, 4), 4),
    (RSP_DEFAULT + 0x8, mem[3], 4),
    (RSP_DEFAULT + 0xc, mem[2], 4),
]

if __name__ == "__main__":
    if len(argv) < 2:
        print(f"{C.BLUE}[+]{C.NC} Usage: python3 {__file__} <path_to_asm_file>")
        print(challenge_info)
        exit(0)

    code = open(argv[1], 'r').read()
    Checker(init_list, ans_list, code)

```
:::
:::spoiler condition.py
```python
#!/usr/bin/python
from module.checker import *
from module.math import *
from sys import argv

challenge_info = f'''
let a = MEM[RSP+0x0:RSP+0x4]
let b = MEM[RSP+0x4:RSP+0x8]
let c = MEM[RSP+0x8:RSP+0xc]
let d = MEM[RSP+0xc:RSP+0x10]

{C.BLUE}# a, b -> signed 4 btyes integer{C.NC}
if a >= b:
    EAX = a
else:
    EAX = b

{C.BLUE}# c, d -> unsigned 4 btyes integer{C.NC}
if c < d:
    EBX = c
else:
    EBX = d

if c is an odd number:
    ECX = c // 8
else:
    ECX = c * 4
'''

a = get_rand(4)
b = get_rand(4)
c = get_rand(4)
d = get_rand(4)


init_list = [
    (RSP_DEFAULT + 0x0, a, 4),
    (RSP_DEFAULT + 0x4, b, 4),
    (RSP_DEFAULT + 0x8, c, 4),
    (RSP_DEFAULT + 0xc, d, 4),
]

a = u2signed(a, 4)
b = u2signed(b, 4)
_eax = (a if a >= b else b) & mask(4)
_ebx = (c if c < d else d) & mask(4)
_ecx = div(c, 8, 4) if is_odd(c) else mul(c, 4, 4)

ans_list = [
    ("eax", _eax),
    ("ebx", _ebx),
    ("ecx", _ecx),
]

if __name__ == "__main__":
    if len(argv) < 2:
        print(f"{C.BLUE}[+]{C.NC} Usage: python3 {__file__} <path_to_asm_file>")
        print(challenge_info)
        exit(0)

    code = open(argv[1], 'r').read()
    Checker(init_list, ans_list, code)


```
:::
## Recon
這一題有三小題，包含`arithmatic.py`, `data_movement.py`, 以及`condition.py`，過關的條件是要自己寫assembly然後達帶這三個關卡的register或stack條件，我是直接用compiler explorer幫我把c code直接轉assembly然後再利用assembly x86 emulator做double check，速度應該會快很多
## Exploit
* 題目一: 就是一般的運算(\+\-*/)
    ```
    let a = MEM[RSP+0x0:RSP+0x4]
    let b = MEM[RSP+0x4:RSP+0x8]
    let c = MEM[RSP+0x8:RSP+0xc]

    EAX = a + b
    EBX = a - b
    ECX = -c
    EDX = 9*a + 7
    ```
    :::spoiler Solution
    ```asm
    mov r8d, dword [rsp] ; 
    mov r9d, dword [rsp + 4] ; 
    mov r10d, dword [rsp + 8] ;

    ; EAX = a + b
    mov eax, r8d
    add eax, r9d

    ; EBX = a - b
    mov ecx, r8d
    sub ecx, r9d
    mov ebx, ecx

    ; ECX = -c
    mov ecx, r10d
    neg ecx

    ; EDX = 9 * a + 7
    mov edx, DWORD [rsp]
    sal edx, 3
    add edx, DWORD [rsp]
    add edx, 7
    ```
    :::
* 題目二: 這邊是考register和stack之間的搬運和運算
    ```
    # Modify register value
    RAX += 0x87
    RBX -= 0x63
    RCX, RDX = RDX, RCX

    {C.BLUE}# Modify memory value
    MEM[RSP+0x0:RSP+0x4] += 0xdeadbeef
    MEM[RSP+0x4:RSP+0x8] -= 0xfaceb00c
    MEM[RSP+0x8:RSP+0xc], MEM[RSP+0xc:RSP+0x10] = MEM[RSP+0xc:RSP+0x10], MEM[RSP+0x8:RSP+0xc]
    ```
    :::spoiler Solution
    ```asm
    ; Modify register value
    add rax, 0x87
    sub rbx, 0x63
    mov r8, rcx
    mov rcx, rdx
    mov rdx, r8

    ; MEM[RSP+0x0:RSP+0x4] += 0xdeadbeef
    mov r8d, dword [rsp]
    add r8d, 0xdeadbeef
    mov dword [rsp], r8d

    ; MEM[RSP+0x4:RSP+0x8] -= 0xfaceb00c
    mov r8d, dword [rsp+4]
    sub r8d, 0xfaceb00c
    mov dword [rsp+4], r8d

    ; MEM[RSP+0x8:RSP+0xc], MEM[RSP+0xc:RSP+0x10] = MEM[RSP+0xc:RSP+0x10], MEM[RSP+0x8:RSP+0xc]
    mov r8d, dword [rsp+8]
    mov r9d, dword [rsp+0xc]
    mov dword [rsp+8], r9d
    mov dword [rsp+0xc], r8d
    ```
    :::
* 題目三: 需要考慮condition，然後看要跳轉到哪邊，重點是jump有分signed和unsigned，而仔細看source code他只有考慮unsinged，所以我們要特別挑選[jump的類別](https://redirect.cs.umbc.edu/courses/undergraduate/CMSC313/spring04/burt_katz/lectures/Lect05/unsignedCondJumps.html)
    ```
    let a = MEM[RSP+0x0:RSP+0x4]
    let b = MEM[RSP+0x4:RSP+0x8]
    let c = MEM[RSP+0x8:RSP+0xc]
    let d = MEM[RSP+0xc:RSP+0x10]

    # a, b -> signed 4 btyes integer
    if a >= b:
        EAX = a
    else:
        EAX = b

    # c, d -> unsigned 4 btyes integer{C.NC}
    if c < d:
        EBX = c
    else:
        EBX = d

    if c is an odd number:
        ECX = c // 8
    else:
        ECX = c * 4
    ```
    :::spoiler Solution
    ```asm
    ; if a >= b:
    ;     EAX = a
    ; else:
    ;     EAX = b
        mov     eax, DWORD [rsp]
        cmp     eax, DWORD [rsp+4]
        jl      L2
        mov     eax, DWORD [rsp]
        jmp     L3
    L2:
        mov     eax, DWORD [rsp+4]


    ; if c < d:
    ;     EBX = c
    ; else:
    ;     EBX = d
    L3:
        mov     edi, DWORD [esp+0x8]
        mov 	esi, DWORD [esp+0xc]
        cmp     edi, esi
        jae     L4
        mov     ebx, DWORD [esp+0x8]
        jmp     L5
    L4:
        mov     ebx, DWORD [esp+0xc]


    ; if c is an odd number:
    ;     ECX = c // 8
    ; else:
    ;     ECX = c * 4
    L5:
        mov     edi, DWORD [esp+0x8]
        and     edi, 1
        cmp     edi, 1
        jne     L6
        mov     ecx, dword [esp+0x8]
        sar     ecx, 3
        jmp     L7
    L6:
        mov     ecx, dword [esp+0x8]
        sal     ecx, 2

    L7:
    ```
    :::

```bash
$ (cat arithmatic.asm | base64 -w0 ; echo '' ; cat data_movement.asm | base64 -w0 ; echo '' ; cat condition.asm | base64 -w0 ; echo '') > answer.txt
$ cat answer.txt | nc edu-ctf.zoolab.org 10020
```

:::spoiler 完整的輸出結果
```bash
cat answer.txt | nc edu-ctf.zoolab.org 10020

──── Challenge Info ──────────────────────────────────────────────

let a = MEM[RSP+0x0:RSP+0x4]
let b = MEM[RSP+0x4:RSP+0x8]
let c = MEM[RSP+0x8:RSP+0xc]

EAX = a + b
EBX = a - b
ECX = -c
EDX = 9*a + 7

Give me your base64 of your assembly code!
>
──── Your Assembly ───────────────────────────────────────────────
mov r8d, dword [rsp] ;
mov r9d, dword [rsp + 4] ;
mov r10d, dword [rsp + 8] ;

; EAX = a + b
mov eax, r8d
add eax, r9d

; EBX = a - b
mov ecx, r8d
sub ecx, r9d
mov ebx, ecx

; ECX = -c
mov ecx, r10d
neg ecx

; EDX = 9 * a + 7
mov edx, DWORD [rsp]
sal edx, 3
add edx, DWORD [rsp]
add edx, 7

([68, 139, 4, 36, 68, 139, 76, 36, 4, 68, 139, 84, 36, 8, 68, 137, 192, 68, 1, 200, 68, 137, 193, 68, 41, 201, 137, 203, 68, 137, 209, 247, 217, 139, 20, 36, 193, 226, 3, 3, 20, 36, 131, 194, 7], 44)
[ Initial Context ]

──── register ────────────────────────────────────────────────────
$rax: 0x0000000000000000
$rbx: 0x0000000000000000
$rcx: 0x0000000000000000
$rdx: 0x0000000000000000
$rdi: 0x0000000000000000
$rsi: 0x0000000000000000
$rbp: 0x0000000000000000
$rsp: 0x0000000007100000

──── stack ───────────────────────────────────────────────────────
0x7100000|+0x0000: 0x3ad14697f68546bc     ← $rsp
0x7100008|+0x0008: 0x00000000aa428281
0x7100010|+0x0010: 0x0000000000000000
0x7100018|+0x0018: 0x0000000000000000
0x7100020|+0x0020: 0x0000000000000000
0x7100028|+0x0028: 0x0000000000000000
0x7100030|+0x0030: 0x0000000000000000
0x7100038|+0x0038: 0x0000000000000000

[ Final Context ]

──── register ────────────────────────────────────────────────────
$rax: 0x0000000031568d53
$rbx: 0x00000000bbb40025
$rcx: 0x0000000055bd7d7f
$rdx: 0x00000000aaaf7ca3
$rdi: 0x0000000000000000
$rsi: 0x0000000000000000
$rbp: 0x0000000000000000
$rsp: 0x0000000007100000

──── stack ───────────────────────────────────────────────────────
0x7100000|+0x0000: 0x3ad14697f68546bc     ← $rsp
0x7100008|+0x0008: 0x00000000aa428281
0x7100010|+0x0010: 0x0000000000000000
0x7100018|+0x0018: 0x0000000000000000
0x7100020|+0x0020: 0x0000000000000000
0x7100028|+0x0028: 0x0000000000000000
0x7100030|+0x0030: 0x0000000000000000
0x7100038|+0x0038: 0x0000000000000000

──── Result ──────────────────────────────────────────────────────
[O] $eax = 0x31568d53
[O] $ebx = 0xbbb40025
[O] $ecx = 0x55bd7d7f
[O] $edx = 0xaaaf7ca3
[+] CORRECT :)

──── Challenge Info ──────────────────────────────────────────────

# Modify register value
RAX += 0x87
RBX -= 0x63
RCX, RDX = RDX, RCX

# Modify memory value
MEM[RSP+0x0:RSP+0x4] += 0xdeadbeef
MEM[RSP+0x4:RSP+0x8] -= 0xfaceb00c
MEM[RSP+0x8:RSP+0xc], MEM[RSP+0xc:RSP+0x10] = MEM[RSP+0xc:RSP+0x10], MEM[RSP+0x8:RSP+0xc]

Give me your base64 of your assembly code!
>
──── Your Assembly ───────────────────────────────────────────────
; Modify register value
add rax, 0x87
sub rbx, 0x63
mov r8, rcx
mov rcx, rdx
mov rdx, r8



; MEM[RSP+0x0:RSP+0x4] += 0xdeadbeef
mov r8d, dword [rsp]
add r8d, 0xdeadbeef
mov dword [rsp], r8d

; MEM[RSP+0x4:RSP+0x8] -= 0xfaceb00c
mov r8d, dword [rsp+4]
sub r8d, 0xfaceb00c
mov dword [rsp+4], r8d

; MEM[RSP+0x8:RSP+0xc], MEM[RSP+0xc:RSP+0x10] = MEM[RSP+0xc:RSP+0x10], MEM[RSP+0x8:RSP+0xc]
mov r8d, dword [rsp+8]
mov r9d, dword [rsp+0xc]
mov dword [rsp+8], r9d
mov dword [rsp+0xc], r8d
([72, 5, 135, 0, 0, 0, 72, 131, 235, 99, 73, 137, 200, 72, 137, 209, 76, 137, 194, 68, 139, 4, 36, 65, 129, 192, 239, 190, 173, 222, 68, 137, 4, 36, 68, 139, 68, 36, 4, 65, 129, 232, 12, 176, 206, 250, 68, 137, 68, 36, 4, 68, 139, 68, 36, 8, 68, 139, 76, 36, 12, 68, 137, 76, 36, 8, 68, 137, 68, 36, 12], 47)
[ Initial Context ]

──── register ────────────────────────────────────────────────────
$rax: 0xd9efd9c16a5bc322
$rbx: 0xb9cf8db36cbfc14a
$rcx: 0x938ee6ed0bf25e63
$rdx: 0xead92779318623a4
$rdi: 0x0000000000000000
$rsi: 0x0000000000000000
$rbp: 0x0000000000000000
$rsp: 0x0000000007100000

──── stack ───────────────────────────────────────────────────────
0x7100000|+0x0000: 0xfc969827aea7be89     ← $rsp
0x7100008|+0x0008: 0x6482df8494b54caf
0x7100010|+0x0010: 0x0000000000000000
0x7100018|+0x0018: 0x0000000000000000
0x7100020|+0x0020: 0x0000000000000000
0x7100028|+0x0028: 0x0000000000000000
0x7100030|+0x0030: 0x0000000000000000
0x7100038|+0x0038: 0x0000000000000000

[ Final Context ]

──── register ────────────────────────────────────────────────────
$rax: 0xd9efd9c16a5bc3a9
$rbx: 0xb9cf8db36cbfc0e7
$rcx: 0xead92779318623a4
$rdx: 0x938ee6ed0bf25e63
$rdi: 0x0000000000000000
$rsi: 0x0000000000000000
$rbp: 0x0000000000000000
$rsp: 0x0000000007100000

──── stack ───────────────────────────────────────────────────────
0x7100000|+0x0000: 0x01c7e81b8d557d78     ← $rsp
0x7100008|+0x0008: 0x94b54caf6482df84
0x7100010|+0x0010: 0x0000000000000000
0x7100018|+0x0018: 0x0000000000000000
0x7100020|+0x0020: 0x0000000000000000
0x7100028|+0x0028: 0x0000000000000000
0x7100030|+0x0030: 0x0000000000000000
0x7100038|+0x0038: 0x0000000000000000

──── Result ──────────────────────────────────────────────────────
[O] $rax = 0xd9efd9c16a5bc3a9
[O] $rbx = 0xb9cf8db36cbfc0e7
[O] $rcx = 0xead92779318623a4
[O] $rdx = 0x938ee6ed0bf25e63
[O] [0x077100000] = 0x8d557d78
[O] [0x077100004] = 0x1c7e81b
[O] [0x077100008] = 0x6482df84
[O] [0x07710000c] = 0x94b54caf
[+] CORRECT :)

──── Challenge Info ──────────────────────────────────────────────

let a = MEM[RSP+0x0:RSP+0x4]
let b = MEM[RSP+0x4:RSP+0x8]
let c = MEM[RSP+0x8:RSP+0xc]
let d = MEM[RSP+0xc:RSP+0x10]

# a, b -> signed 4 btyes integer
if a >= b:
    EAX = a
else:
    EAX = b

# c, d -> unsigned 4 btyes integer
if c < d:
    EBX = c
else:
    EBX = d

if c is an odd number:
    ECX = c // 8
else:
    ECX = c * 4

Give me your base64 of your assembly code!
>
──── Your Assembly ───────────────────────────────────────────────
; if a >= b:
;     EAX = a
; else:
;     EAX = b
    mov     eax, DWORD [rsp]
    cmp     eax, DWORD [rsp+4]
    jl      L2
    mov     eax, DWORD [rsp]
    jmp     L3
L2:
    mov     eax, DWORD [rsp+4]


; if c < d:
;     EBX = c
; else:
;     EBX = d
L3:
        mov     edi, DWORD [esp+0x8]
        mov     esi, DWORD [esp+0xc]
    cmp     edi, esi
    jae     L4
    mov     ebx, DWORD [esp+0x8]
    jmp     L5
L4:
    mov     ebx, DWORD [esp+0xc]


; if c is an odd number:
;     ECX = c // 8
; else:
;     ECX = c * 4
L5:
        mov     edi, DWORD [esp+0x8]
        and     edi, 1
        cmp     edi, 1
        jne     L6
        mov     ecx, dword [esp+0x8]
        sar     ecx, 3
        jmp     L7
L6:
        mov     ecx, dword [esp+0x8]
        sal     ecx, 2

L7:
([139, 4, 36, 59, 68, 36, 4, 124, 5, 139, 4, 36, 235, 4, 139, 68, 36, 4, 103, 139, 124, 36, 8, 103, 139, 116, 36, 12, 57, 247, 115, 7, 103, 139, 92, 36, 8, 235, 5, 103, 139, 92, 36, 12, 103, 139, 124, 36, 8, 131, 231, 1, 131, 255, 1, 117, 10, 103, 139, 76, 36, 8, 193, 249, 3, 235, 8, 103, 139, 76, 36, 8, 193, 225, 2], 89)
[ Initial Context ]

──── register ────────────────────────────────────────────────────
$rax: 0x0000000000000000
$rbx: 0x0000000000000000
$rcx: 0x0000000000000000
$rdx: 0x0000000000000000
$rdi: 0x0000000000000000
$rsi: 0x0000000000000000
$rbp: 0x0000000000000000
$rsp: 0x0000000007100000

──── stack ───────────────────────────────────────────────────────
0x7100000|+0x0000: 0x21bd1f6bf4090a3a     ← $rsp
0x7100008|+0x0008: 0xfd382fd2ccd74eca
0x7100010|+0x0010: 0x0000000000000000
0x7100018|+0x0018: 0x0000000000000000
0x7100020|+0x0020: 0x0000000000000000
0x7100028|+0x0028: 0x0000000000000000
0x7100030|+0x0030: 0x0000000000000000
0x7100038|+0x0038: 0x0000000000000000

[ Final Context ]

──── register ────────────────────────────────────────────────────
$rax: 0x0000000021bd1f6b
$rbx: 0x00000000ccd74eca
$rcx: 0x00000000335d3b28
$rdx: 0x0000000000000000
$rdi: 0x0000000000000000
$rsi: 0x00000000fd382fd2
$rbp: 0x0000000000000000
$rsp: 0x0000000007100000

──── stack ───────────────────────────────────────────────────────
0x7100000|+0x0000: 0x21bd1f6bf4090a3a     ← $rsp
0x7100008|+0x0008: 0xfd382fd2ccd74eca
0x7100010|+0x0010: 0x0000000000000000
0x7100018|+0x0018: 0x0000000000000000
0x7100020|+0x0020: 0x0000000000000000
0x7100028|+0x0028: 0x0000000000000000
0x7100030|+0x0030: 0x0000000000000000
0x7100038|+0x0038: 0x0000000000000000

──── Result ──────────────────────────────────────────────────────
[O] $eax = 0x21bd1f6b
[O] $ebx = 0xccd74eca
[O] $ecx = 0x335d3b28
[+] CORRECT :)

──── Your Flag ───────────────────────────────────────────────────
Congrats! You passed all challenges! Here is your flag:  FLAG{c0d1Ng_1n_a5s3mB1y_i5_sO_fun!}
```
:::

Flag: `FLAG{c0d1Ng_1n_a5s3mB1y_i5_sO_fun!}`