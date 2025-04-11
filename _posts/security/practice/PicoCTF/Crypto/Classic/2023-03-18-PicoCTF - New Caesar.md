---
title: PicoCTF - New Caesar
tags: [PicoCTF, CTF, Crypto]

category: "Security/Practice/PicoCTF/Crypto/Classic"
---

# PicoCTF - New Caesar
###### tags: `PicoCTF` `CTF` `Crypto`
Challenge: [New Caesar](https://play.picoctf.org/practice/challenge/158?category=2&page=1)

## Source code
::: spoiler source code
```python=
import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

def b16_encode(plain):
	enc = ""
	for c in plain:
		binary = "{0:08b}".format(ord(c))
		enc += ALPHABET[int(binary[:4], 2)]
		enc += ALPHABET[int(binary[4:], 2)]
	return enc

def shift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET
	t2 = ord(k) - LOWERCASE_OFFSET
	return ALPHABET[(t1 + t2) % len(ALPHABET)]

flag = "redacted"
key = "redacted"
assert all([k in ALPHABET for k in key])
assert len(key) == 1

b16 = b16_encode(flag)
enc = ""
for i, c in enumerate(b16):
	enc += shift(c, key[i % len(key)])
print(enc)

```
:::
## Recon
1. Hint in the code
It gave two hints in the code that represented by `assert`
    1.1 The key must in the first 16 character of alphabet strings, that is, the key is composed of `a~p`.
    1.2 The key length is just 1
2. Encode to binary
Then it encodes each character to hex and split it in the middle. Then map the value to alphabet sequence, that is, 
`a` $\to$ `0`
`b` $\to$ `1`
...
`o` $\to$ `14`
`p` $\to$ `15`
3. Shift string
This process is just like `rot n` that it shift the concatenated strings with `n` characters.

## Exploit - Recover
1. Guess it shift `n` character
First, we can guess the `n` value for example 1. And then we try to shift it back.
2. Regroup and Re-mapping
Then we can represent the shifted string as binary. If the length of the binary value is equal to `8`, that means we can regroup it to a real strings as ascii.
3. Then repeat 16 times
Here is the 16 outcomes...
    ```bash
    et_tu?_23217b54456fb10e908b5e87c6e89156
    v`@`CDCBHsFEEFGwsBAvJAIsFvIHtGvIJBFG
    qQqTUTSYWVVWXSR[RZWZYXZ[SWX
    §§¨befedjhgghidclckhkjikldhi
    ©¸¸¹svwvu{¦yxxyzª¦ut©}t|¦y©|{§z©|}uyz
    ºÉ¤ÉÊ¤·»·º·º¸º
    ËÚµÚÛµÈÌÈËÈËÉË
    ÜëÆëì¦Æ©ª©¨®Ù¬««¬­ÝÙ¨§Ü §¯Ù¬Ü¯®Ú­Ü¯ ¨¬­
    íü×üý·×º»º¹¿ê½¼¼½¾îê¹¸í±¸°ê½í°¿ë¾í°±¹½¾
    ÈèËÌËÊÀûÎÍÍÎÏÿûÊÉþÂÉÁûÎþÁÀüÏþÁÂÊÎÏ
    ```
    Seems the first one is quite normal. And we got the flag...
    Flag: `picoCTF{et_tu?_23217b54456fb10e908b5e87c6e89156}`
:::spoiler whole exploit
```python!=
import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]
cipher_flag = "apbopjbobpnjpjnmnnnmnlnbamnpnononpnaaaamnlnkapndnkncamnpapncnbannaapncndnlnpna"

def binToHexa(n):
    bnum = int(n)
    temp = 0
    mul = 1
    count = 1
    hexaDeciNum = ['0'] * 100
    i = 0
    while bnum != 0:
        rem = bnum % 10
        temp = temp + (rem*mul)
        if count % 4 == 0:
            if temp < 10:
                hexaDeciNum[i] = chr(temp+48)
            else:
                hexaDeciNum[i] = chr(temp+55)
            mul = 1
            temp = 0
            count = 1
            i = i+1
        else:
            mul = mul*2
            count = count+1
        bnum = int(bnum/10)
    if count != 1:
        hexaDeciNum[i] = chr(temp+48)
    if count == 1:
        i = i-1
    hex_string = ''
    while i >= 0:
        hex_string += hexaDeciNum[i]
        i = i-1
    if hex_string == '':
        hex_string = '00'
    return hex_string

tmp = ""
guess_strings = ""
for i in range(1, 16):
    for e in cipher_flag:
        tmp += "{0:04b}".format((ord(e) - LOWERCASE_OFFSET + i) % len(ALPHABET))
        if len(tmp) % 8 == 0:
            guess_strings += chr(int(binToHexa(tmp), 16))
            tmp = ""
    tmp = ""
    print(guess_strings)
    guess_strings = ""
:::