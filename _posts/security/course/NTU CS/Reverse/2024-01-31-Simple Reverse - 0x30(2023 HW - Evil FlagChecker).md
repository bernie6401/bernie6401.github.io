---
title: Simple Reverse - 0x30(2023 HW - Evil FlagChecker)
tags: [eductf, CTF, Reverse]

category: "Security/Course/NTU CS/Reverse"
---

# Simple Reverse - 0x30(2023 HW - Evil FlagChecker)

## Background
Anti Disassembly - 這一部分可以看一下碩一修的malware reverse的anti disassembly的修復(就是d和c的交錯使用)
Anti Debugging - 首推scylla hide

## Source code
:::spoiler IDA main
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  DWORD TickCount; // [esp+0h] [ebp-14h]
  unsigned int v5; // [esp+8h] [ebp-Ch]

  TickCount = GetTickCount();
  Sleep(120000u);
  v5 = GetTickCount() - TickCount;
  if ( v5 < 119950 || v5 > 120050 )
    ExitProcess(0);
  ((void (*)(void))loc_401AE0)();
  return 0;
}
```
:::
:::spoiler IDA loc_401AE0
```
.text:00401AE0 loc_401AE0:                             ; CODE XREF: _main:loc_4014AB↑p
.text:00401AE0 push    ebp
.text:00401AE1 mov     ebp, esp
.text:00401AE3 lea     esi, aHelloHacker               ; "Hello Hacker"
.text:00401AE9 mov     al, 48h ; 'H'
.text:00401AEB cmp     [esi], al
.text:00401AED jz      short loc_401AF0
.text:00401AED
.text:00401AED ; ---------------------------------------------------------------------------
.text:00401AEF db 0E8h
.text:00401AF0 ; ---------------------------------------------------------------------------
.text:00401AF0
.text:00401AF0 loc_401AF0:                             ; CODE XREF: .text:00401AED↑j
.text:00401AF0 nop     word ptr [eax+eax+00000000h]
.text:00401AF9 jmp     short loc_401B01
.text:00401AF9
.text:00401AF9 ; ---------------------------------------------------------------------------
.text:00401AFB db  48h ; H
.text:00401AFC db  65h ; e
.text:00401AFD db  6Ch ; l
.text:00401AFE db  6Ch ; l
.text:00401AFF db  6Fh ; o
.text:00401B00 db    0
.text:00401B01 ; ---------------------------------------------------------------------------
.text:00401B01
.text:00401B01 loc_401B01:                             ; CODE XREF: .text:00401AF9↑j
.text:00401B01 jmp     short loc_401B0E
.text:00401B01
.text:00401B01 ; ---------------------------------------------------------------------------
.text:00401B03 db 0E8h
.text:00401B04 db  66h ; f
.text:00401B05 db  0Fh
.text:00401B06 db  1Fh
.text:00401B07 db  84h
.text:00401B08 db    0
.text:00401B09 db    0
.text:00401B0A db    0
.text:00401B0B db    0
.text:00401B0C byte_401B0C db 0
.text:00401B0D db 0E8h
.text:00401B0E ; ---------------------------------------------------------------------------
.text:00401B0E
.text:00401B0E loc_401B0E:                             ; CODE XREF: .text:loc_401B01↑j
.text:00401B0E jz      short loc_401B13
.text:00401B0E
.text:00401B10 jnz     short loc_401B13
.text:00401B10
.text:00401B10 ; ---------------------------------------------------------------------------
.text:00401B12 db 0E8h
.text:00401B13 ; ---------------------------------------------------------------------------
.text:00401B13
.text:00401B13 loc_401B13:                             ; CODE XREF: .text:loc_401B0E↑j
.text:00401B13                                         ; .text:00401B10↑j
.text:00401B13 push    1
.text:00401B15 jmp     sub_401220
```
:::
:::spoiler IDA notify_debugger
```cpp
void __cdecl __noreturn notify_debugger()
{
  if ( IsDebuggerPresent() )
    ExitProcess(1u);
  __debugbreak();
}
```
:::
:::spoiler IDA sub_401220
```
.text:00401220 sub_401220 proc near                    ; CODE XREF: .text:00401B15↓j
.text:00401220
.text:00401220 ms_exc= CPPEH_RECORD ptr -18h
.text:00401220
.text:00401220 push    ebp
.text:00401221 mov     ebp, esp
.text:00401223 push    0FFFFFFFEh
.text:00401225 push    offset stru_403B40
.text:0040122A push    offset ?notify_debugger@@YAXABUtagEXCEPTION_VISUALCPP_DEBUG_INFO@@@Z_SEH
.text:0040122F mov     eax, large fs:0
.text:00401235 push    eax
.text:00401236 sub     esp, 8
.text:00401239 push    ebx
.text:0040123A push    esi
.text:0040123B push    edi
.text:0040123C mov     eax, ___security_cookie
.text:00401241 xor     [ebp+ms_exc.registration.ScopeTable], eax
.text:00401244 xor     eax, ebp
.text:00401246 push    eax
.text:00401247 lea     eax, [ebp+ms_exc.registration]
.text:0040124A mov     large fs:0, eax
.text:00401250 mov     [ebp+ms_exc.old_esp], esp
.text:00401253 mov     [ebp+ms_exc.registration.TryLevel], 0
.text:0040125A call    sub_401170
.text:0040125A
.text:0040125F ; ---------------------------------------------------------------------------
.text:0040125F test    al, al
.text:00401261 jz      short loc_40126B
.text:00401261
.text:00401263 push    1                               ; uExitCode
.text:00401265 call    ds:ExitProcess
.text:00401265
.text:0040126B ; ---------------------------------------------------------------------------
.text:0040126B
.text:0040126B loc_40126B:                             ; CODE XREF: sub_401220+41↑j
.text:0040126B int     3                               ; Trap to Debugger
.text:0040126B
.text:0040126C ; ---------------------------------------------------------------------------
.text:0040126C jmp     short loc_40127C
.text:0040126C
.text:0040126E ; ---------------------------------------------------------------------------
.text:0040126E
.text:0040126E loc_40126E:                             ; DATA XREF: .rdata:stru_403B40↓o
.text:0040126E mov     eax, 1
.text:00401273 retn
.text:00401273
.text:00401274 ; ---------------------------------------------------------------------------
.text:00401274
.text:00401274 loc_401274:                             ; DATA XREF: .rdata:stru_403B40↓o
.text:00401274 mov     esp, [ebp+ms_exc.old_esp]
.text:00401277 call    ?notify_debugger@@YAXABUtagEXCEPTION_VISUALCPP_DEBUG_INFO@@@Z ; notify_debugger(tagEXCEPTION_VISUALCPP_DEBUG_INFO const &)
.text:00401277
.text:0040127C ; ---------------------------------------------------------------------------
.text:0040127C
.text:0040127C loc_40127C:                             ; CODE XREF: sub_401220+4C↑j
.text:0040127C mov     [ebp+ms_exc.registration.TryLevel], 0FFFFFFFEh
.text:00401283 mov     ecx, [ebp+ms_exc.registration.Next]
.text:00401286 mov     large fs:0, ecx
.text:0040128D pop     ecx
.text:0040128E pop     edi
.text:0040128F pop     esi
.text:00401290 pop     ebx
.text:00401291 mov     esp, ebp
.text:00401293 pop     ebp
.text:00401294 retn
.text:00401294
.text:00401294 sub_401220 endp
```
:::
:::spoiler IDA sub_401170
```
.text:00401170 sub_401170 proc near                    ; CODE XREF: sub_401220+3A↓p
.text:00401170
.text:00401170 var_1= byte ptr -1
.text:00401170
.text:00401170 push    ebp
.text:00401171 mov     ebp, esp
.text:00401173 push    ecx
.text:00401174 mov     [ebp+var_1], 1
.text:00401178 push    offset TopLevelExceptionFilter  ; lpTopLevelExceptionFilter
.text:0040117D call    ds:SetUnhandledExceptionFilter
.text:0040117D
.text:00401183 ; ---------------------------------------------------------------------------
.text:00401183 int     3                               ; Trap to Debugger
.text:00401183
.text:00401183 sub_401170 endp
.text:00401183
.text:00401184 ; ---------------------------------------------------------------------------
.text:00401184 jmp     short loc_40118A
.text:00401184
.text:00401186 ; ---------------------------------------------------------------------------
.text:00401186 mov     byte ptr [ebp-1], 0
.text:00401186
.text:0040118A
.text:0040118A loc_40118A:                             ; CODE XREF: .text:00401184↑j
.text:0040118A mov     al, [ebp-1]
.text:0040118D mov     esp, ebp
.text:0040118F pop     ebp
.text:00401190 retn
.text:00401190
.text:00401190 ; ---------------------------------------------------------------------------
.text:00401191 align 10h
.text:004011A0
.text:004011A0 ; =============== S U B R O U T I N E =======================================
.text:004011A0
.text:004011A0 ; Attributes: library function noreturn static bp-based frame
.text:004011A0
.text:004011A0 ; void __cdecl __noreturn notify_debugger()
.text:004011A0 ?notify_debugger@@YAXABUtagEXCEPTION_VISUALCPP_DEBUG_INFO@@@Z proc near
.text:004011A0                                         ; CODE XREF: sub_401220+57↓p
.text:004011A0
.text:004011A0 ms_exc= CPPEH_RECORD ptr -18h
.text:004011A0
.text:004011A0 ; FUNCTION CHUNK AT .text:00401206 SIZE 0000000E BYTES
.text:004011A0
.text:004011A0 push    ebp
.text:004011A1 mov     ebp, esp
.text:004011A3 push    0FFFFFFFEh
.text:004011A5 push    offset stru_403B20
.text:004011AA push    offset ?notify_debugger@@YAXABUtagEXCEPTION_VISUALCPP_DEBUG_INFO@@@Z_SEH
.text:004011AF mov     eax, large fs:0
.text:004011B5 push    eax
.text:004011B6 sub     esp, 8
.text:004011B9 push    ebx
.text:004011BA push    esi
.text:004011BB push    edi
.text:004011BC mov     eax, ___security_cookie
.text:004011C1 xor     [ebp+ms_exc.registration.ScopeTable], eax
.text:004011C4 xor     eax, ebp
.text:004011C6 push    eax
.text:004011C7 lea     eax, [ebp+ms_exc.registration]
.text:004011CA mov     large fs:0, eax
.text:004011D0 mov     [ebp+ms_exc.old_esp], esp
.text:004011D3 mov     [ebp+ms_exc.registration.TryLevel], 0
.text:004011DA call    ds:IsDebuggerPresent
.text:004011DA
.text:004011E0 test    eax, eax
.text:004011E2 jz      short loc_4011EC
.text:004011E2
.text:004011E4 push    1                               ; uExitCode
.text:004011E6 call    ds:ExitProcess
.text:004011E6
.text:004011EC ; ---------------------------------------------------------------------------
.text:004011EC
.text:004011EC loc_4011EC:                             ; CODE XREF: notify_debugger(tagEXCEPTION_VISUALCPP_DEBUG_INFO const &)+42↑j
.text:004011EC int     3                               ; Trap to Debugger
.text:004011EC
.text:004011EC ?notify_debugger@@YAXABUtagEXCEPTION_VISUALCPP_DEBUG_INFO@@@Z endp
.text:004011EC
.text:004011ED ; ---------------------------------------------------------------------------
.text:004011ED mov     dword ptr [ebp-4], 0FFFFFFFEh
.text:004011F4 mov     ecx, [ebp-10h]
.text:004011F7 mov     large fs:0, ecx
.text:004011FE pop     ecx
.text:004011FF pop     edi
.text:00401200 pop     esi
.text:00401201 pop     ebx
.text:00401202 mov     esp, ebp
.text:00401204 pop     ebp
.text:00401205 retn
.text:00401205
.text:00401206 ; ---------------------------------------------------------------------------
.text:00401206 ; START OF FUNCTION CHUNK FOR notify_debugger(tagEXCEPTION_VISUALCPP_DEBUG_INFO const &)
.text:00401206
.text:00401206 loc_401206:                             ; DATA XREF: .rdata:stru_403B20↓o
.text:00401206 mov     eax, 1
.text:0040120B retn
.text:0040120B
.text:0040120C ; ---------------------------------------------------------------------------
.text:0040120C
.text:0040120C loc_40120C:                             ; DATA XREF: .rdata:stru_403B20↓o
.text:0040120C mov     esp, [ebp+ms_exc.old_esp]
.text:0040120F call    InputFlag_Check
```
:::
:::spoiler IDA InputFlag_Check
```cpp
void __noreturn InputFlag_Check()
{
  flag_info flag_info; // [esp+0h] [ebp-408h] BYREF

  printf(flag_info.Hello, flag_info.nonono);
  memset(&flag_info, 0, sizeof(flag_info));
  scanf(std::cin, (int)&flag_info);
  check((int)&flag_info, strlen((const char *)&flag_info));
  printf(flag_info.Hello, flag_info.nonono);
  ExitProcess(0);
}
```
:::
:::spoiler IDA check
```cpp
void __fastcall check(char *input, unsigned int len)
{
  unsigned int iv; // ebx
  unsigned int block; // edi
  int mem_addr_gap; // ecx
  unsigned __int8 cipher; // cl
  char *input_cipher_cp; // ecx
  char *cipher_flag_cp; // edx
  bool v9; // cf
  unsigned int i; // esi
  int dot; // [esp+0h] [ebp-41Ch]
  int new_line; // [esp+4h] [ebp-418h]
  int mem_addr_gap_cp; // [esp+Ch] [ebp-410h]
  char output[1028]; // [esp+10h] [ebp-40Ch] BYREF

  iv = 0xE0C92EAB;
  memset(output, 0, 0x400u);
  block = 0;
  if ( len )
  {
    mem_addr_gap = input - output;              // v5代表我們輸入的flag的位址和他memset的位址的差距，從這支檔案為例就是0x418
    mem_addr_gap_cp = input - output;
    do
    {
      cipher = iv ^ output[block + mem_addr_gap];
      output[block] = cipher;
      iv = len + (cipher ^ __ROR4__(iv, 3)) - block;
      Sleep(1000u);
      printf(dot, new_line);
      mem_addr_gap = mem_addr_gap_cp;
      ++block;
    }
    while ( block < len );
  }
  printf(dot, new_line);
  input_cipher_cp = output;
  cipher_flag_cp = cipher_flag;
  v9 = len < 4;
  for ( i = len - 4; !v9; i -= 4 )
  {
    if ( *(_DWORD *)input_cipher_cp != *(_DWORD *)cipher_flag_cp )
      break;
    input_cipher_cp += 4;
    cipher_flag_cp += 4;
    v9 = i < 4;
  }
}
```
:::

## Recon
這一題沒有那麼難，難的是怎麼用工具寫出來，本來想要直接用z3或angr直接噴出來，但是不知道為啥就完全沒有奇蹟發生，所以還是硬幹

首先，先用ida看主要的流程，會發現有很多jmp系列的位址都跑掉了，此時就要修復，就是data(d)和code( c)之間交錯使用，並且把那些奇怪的data byte換成nop，修把patch好的部分，就會呈現上面的source code這樣

1. 一樣由上而下，首先會先進到sleep睡眠兩分鐘，並且判斷進到下一行的時候，時間是否在範圍內，這也是time based的anti debugging手法，這部分可以動態直接patch掉
    :::spoiler Patch Sleep Function Result
    ![圖片](https://hackmd.io/_uploads/SkPJKTiN6.png)
    ![圖片](https://hackmd.io/_uploads/ByKlFaiN6.png)
    :::
2. 接著會進到loc_401AE0，這部分應該是一個function但不知道為甚麼IDA翻譯不出來，不過看了一下source code也是蠻簡單的，就是一直跳到==sub_401220==，這個在動態也可以patch
    :::spoiler Patch Anti-Debug Result
    ![圖片](https://hackmd.io/_uploads/r15VqajVa.png)
    :::
3. ==sub_401220==主要是在其他anti debug的部分，具體怎麼做不是很清楚，只知道大概是和exception handler有關係，不過我在開了scylla hide之後沒有出現甚麼特別的事情
    ![圖片](https://hackmd.io/_uploads/rySec6jN6.png)
4. 接著會進到==sub_401170==，這一段蠻重要的，就是處理一些Exception Handler的事情，然後莫名其妙的會進到0x40120F中的==InputFlag_Check==，中間的一些操作可能是被scylla hide擋掉了，不過中間也確實有檢察==IsDebuggerPresent==這東西
5. 到了這邊就可以大膽猜測一些常見的操作，諸如scanf或是printf的function，接著我們會進到check這個function，也就是實際把我們的輸入，進行cipher操作後和內部的data bytes進行對比的過程
6. 所以到了這邊一切都很明瞭了，主要的code如下
    ```cpp
      iv = 0xE0C92EAB;
      memset(output, 0, 0x400u);
      block = 0;
      if ( len )
      {
        mem_addr_gap = input - output;              // v5代表我們輸入的flag的位址和他memset的位址的差距，從這支檔案為例就是0x418
        mem_addr_gap_cp = input - output;
        do
        {
          cipher = iv ^ output[block + mem_addr_gap];
          output[block] = cipher;
          iv = len + (cipher ^ __ROR4__(iv, 3)) - block;
          Sleep(1000u);
          printf(dot, new_line);
          mem_addr_gap = mem_addr_gap_cp;
          ++block;
        }
        while ( block < len );
      }
    ```
    其中，`output[block + mem_addr_gap]`其實就是我們的input，所以exploit的邏輯就是用brute force，把所有可能都丟一遍，然後嘗試去對比有沒有和built-in cipher bytes一樣，BTW，`len`代表我們輸入的長度，合理猜測和built-in cipher bytes的長度一樣，也就是23個char，中間的sleep在動態也可以patch掉，就看自己方便
:::danger
在寫ROR的實作時有一個非常重要的重點要注意，也就是最後一個右旋的bit如果是0，在下一次右旋時會被忽略，也就是那個bit會消失，被當成0x的一部分，舉例來說，0x111001，右旋兩次後變成0x011110，但是最左邊的0會被當成0x的一部分，所以下一次再右旋兩次的結果會變成0x10111而不是0x100111，所以我的作法是在每次右旋之前都檢查bit length是不是都是32 bits，如果有少就padding 0在最左邊
:::

## Exploit
另外說明一下，z3或angr的解法都沒辦法實作出來，不確定是甚麼原因，但有機會還是會想解看看，所以先放著看看
```python
from string import *
from tqdm import trange


def ror(n, rotations, width):
    if rotations.bit_length() < 32:
        rotations = '0' * (32 - rotations.bit_length()) + bin(rotations)[2:]
        tmp = rotations[-width:] + rotations[:-width]
        return int(tmp, 2)
    tmp = int(bin(rotations << (n-width))[-n:-n+width] + bin(rotations >> width)[2:], 2)
    return tmp


candidates = printable
targets = [0xED, 0x03, 0x81, 0x69, 0x7B, 0x84, 0xA6, 0xA0, 0x5B, 0x2B, 0xB6, 0xE6, 0x5C, 0x57, 0xC9, 0x99, 0xE8, 0xB2, 0x20, 0x72, 0x38, 0xF1, 0x58]
len = len(targets)
iv = 0xE0C92EAB
flag = ''
for byte in trange(len):
    iv_xor = int(hex(iv)[2:][-2:], 16)
    for candidate in candidates:
        cipher = iv_xor ^ ord(candidate)
        if cipher == targets[byte]:
            flag += candidate
            iv = ror(32, iv, 3)
            iv = len + (cipher ^ iv) - byte
            break
    # print(flag)

print(flag)
```
:::spoiler z3 solver
```python
from z3 import *

target = [0xED, 0x03, 0x81, 0x69, 0x7B, 0x84, 0xA6, 0xA0, 0x5B, 0x2B, 0xB6, 0xE6, 0x5C, 0x57, 0xC9, 0x99, 0xE8, 0xB2, 0x20, 0x72, 0x38, 0xF1, 0x58]
len = len(target)
iv = 0xE0C92EAB
# 起手式 - 開一個Solver
s = Solver()

# 建立符號 - 以此HW來說就是建立23個符號對應每一個flag字元
bvs = [BitVec(f'bt_{i}', 8) for i in range(len)]

# 加上constraint - 以此lab來說每一個flag字元都應該限制在空白到0x7f之間
for bv in bvs:
    s.add(And(bv >= 0x20, bv <= 0x7f))

for i in range(len):
    iv = f'int(hex(iv)[2:][-2:], 16)'
    bvs_formula = f'(({eval(iv)}) ^ bvs[{i}])'
    s.add(eval(bvs_formula) == target[i])
    RotateRight = f'int(bin({iv_formula} << (32-3))[-32:-29] + bin({iv_formula} >> 3)[2:], 2)'
    iv_formula = f'{int(hex(iv)[2:][-2:], 16)}'
    iv_formula = f'{len} + ({iv_formula} ^ {iv}) - {i}'
    print(f'iv_formula = {iv_formula}')

# 如果有解的話就會做以下操作
if s.check() == sat:
    print('Find ~~~')
    print(s.model())

    flag = ""
    for bv in bvs:
        flag += chr(s.model()[bv].as_long())

    print(flag)
```
:::
:::spoiler angr solver
```python
import angr
import claripy

# 建立一個project
root = 'Reverse/HW3/Evil FlagChecker/'
proj = angr.Project(root + 'test.exe')

# 建立Claripy Symbol
sym_arg = claripy.BVS('sym_arg', 8 * 23) # 就像z3一樣要建立symbol

# 建立初始的state
state = proj.factory.entry_state(stdin=sym_arg)
simgr = proj.factory.simulation_manager(state)

# 有了proj/symbol/initial state之後就要開始讓他跑起來
# simgr.explore(find = lambda s: b'Good!' in s.posix.dumps(1))
simgr.explore(find = lambda s: b"Good!" in s.posix.dumps(1), avoid=lambda s: b"No no no..." in s.posix.dumps(1))

if len(simgr.found) > 0:
    print(simgr.found[0].solver.eval(sym_arg, cast_to=bytes))
else:
    print("NONONONO")
```
:::

Flag: `FLAG{jmp1ng_a1l_ar0und}`