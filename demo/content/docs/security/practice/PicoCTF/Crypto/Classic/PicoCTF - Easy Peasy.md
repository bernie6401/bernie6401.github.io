---
title: PicoCTF - Easy Peasy
tags: [PicoCTF, CTF, Crypto]

---

# PicoCTF - Easy Peasy
###### tags: `PicoCTF` `CTF` `Crypto`
Challenge: [Easy Peasy]()

## Background

## Source code
:::spoiler source code
```python=
#!/usr/bin/python3 -u
import os.path

KEY_FILE = "key"
KEY_LEN = 50000
FLAG_FILE = "flag"

def startup(key_location):
	flag = open(FLAG_FILE).read()
	kf = open(KEY_FILE, "rb").read()

	start = key_location
	stop = key_location + len(flag)

	key = kf[start:stop]
	key_location = stop

	result = list(map(lambda p, k: "{:02x}".format(ord(p) ^ k), flag, key))
	print("This is the encrypted flag!\n{}\n".format("".join(result)))

	return key_location

def encrypt(key_location):
	ui = input("What data would you like to encrypt? ").rstrip()
	if len(ui) == 0 or len(ui) > KEY_LEN:
		return -1

	start = key_location
	stop = key_location + len(ui)

	kf = open(KEY_FILE, "rb").read()

	if stop >= KEY_LEN:
		stop = stop % KEY_LEN
		key = kf[start:] + kf[:stop]
	else:
		key = kf[start:stop]
	key_location = stop

	result = list(map(lambda p, k: "{:02x}".format(ord(p) ^ k), ui, key))

	print("Here ya go!\n{}\n".format("".join(result)))

	return key_location


print("******************Welcome to our OTP implementation!******************")
c = startup(0)
while c >= 0:
	c = encrypt(c)

```
:::

## Exploit - Reuse Key
1. Observe the length of key
It's 50000. So, we can reuse it after sending the trash value with length $50000 - len(flag)\ /\ 2$
2. Then send a given strings with length 32
After sending the trash data, we can reuse the key and though we do not know the flag nor key, we can send something with size 32 that we construct ourselves such as `'a' * 32`
The workflow is as below:
$flag\ xor\ key = A$
$\{'a'*32\}\ xor\ key = B$
The exploit is $\to$
$B\ xor\ \{'a'*32\}=key$
$key\ xor\ A=flag$

    So, the whole expression is $B\ xor\ \{'a'*32\}\ xor\ A=flag$

3. These code aimed to find the cipher flag and cipher `'a'*32`
    ```python!=
    from pwn import *
    import sys


    r = remote('mercury.picoctf.net', 11188)
    context.arch = 'amd64'
    r.recvline()
    r.recvline()
    cipher_flag = r.recvlineS(keepends = False)
    log.info(f"Cipher flag: {cipher_flag}")

    r.recvline()
    r.sendline(b'a'*(50000 - int(len(cipher_flag) / 2)))
    r.recvline()
    r.recvline()
    r.recvline()
    r.sendline(b'a' * 32)
    r.recvline()
    encrypt_32a = r.recvlineS(keepends = False)
    log.info(f"Cipher 'a' * 32: {encrypt_32a}")

    plaintext_32a = '61' * 32
    log.info(f"Plaintext 'a' * 32: {plaintext_32a}")

    r.interactive()
    ```
4. Find flag
    ```bash
    $ python
    >>> a = 0x551e6c4c5e55644b56566d1b5100153d4004026a4b52066b4a5556383d4b0007
    >>> b = 0x03463d1959523d1907513d190503163d1903543d1904573d1900003b3d190457
    >>> c = 0x6161616161616161616161616161616161616161616161616161616161616161
    >>> '{:x}'.format(a^b^c)
    '3739303466663833306631633562626138663736333730373234376261336531'
    >>> print(bytes.fromhex(d).decode('utf-8'))
    7904ff830f1c5bba8f763707247ba3e1
    ```
    The flag is **`picoCTF{7904ff830f1c5bba8f763707247ba3e1}`**

## Reference
[picoCTF 2021 easypeasy](https://youtu.be/VodIW2TT_ag)
[Easy Peasy - write up](https://github.com/Dvd848/CTFs/blob/master/2021_picoCTF/Easy_Peasy.md)
