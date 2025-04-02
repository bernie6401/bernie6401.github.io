---
title: PicoCTF - It's Not My Fault 1
tags: [PicoCTF, CTF, Crypto]

---

# PicoCTF - It's Not My Fault 1
###### tags: `PicoCTF` `CTF` `Crypto`

## Background

## Source code
:::spoiler Source code
```python=
#!/usr/bin/python3 -u
import random
import string
import hashlib
import time

from Crypto.Util.number import inverse, getPrime, bytes_to_long, GCD
from sympy.ntheory.modular import solve_congruence

FLAG = open('flag.txt', 'r').read()

def CRT(a, m, b, n):
	val, mod = solve_congruence((a, m), (b, n))
	return val

def gen_key():
	while True:
		p = getPrime(512)
		q = getPrime(512)
		if GCD(p-1, q-1) == 2:
			return p, q

def get_clue(p, q, BITS):
	while True:
		d_p = random.randint(1, 1 << BITS)
		d_q = random.randint(1, q - 1)
		if d_p % 2 == d_q % 2:
			d = CRT(d_p, p - 1, d_q, q - 1)
			e = inverse(d, (p - 1) * (q - 1))
			print("Clue : ", e)
			return

def get_flag(p, q):
	start = time.time()
	ans = int(input())
	if (time.time() - start) > (15 * 60):
		print("Too long!")
		exit()
	else:
		if ans == p + q:
			print(FLAG)
		else:
			print("oops...")


#PoW

vals1 = "".join([random.choice(string.digits) for _ in range(5)])
vals2 = "".join([random.choice(string.hexdigits.lower()) for _ in range(6)])
user_input = input("Enter a string that starts with \"{}\" (no quotes) which creates an md5 hash that ends in these six hex digits: {}\n".format(vals1, vals2))
user_hash = hashlib.md5(user_input.encode()).hexdigest()

if user_input[:5] == vals1 and user_hash[-6:] == vals2:
	p, q = gen_key()
	n = p * q
	print("Public Modulus : ", n)
	get_clue(p, q, 20)
	get_flag(p, q)

```
:::

* 一開始先設立PoW的Challenge，之後才進到RSA的部分
* 可以看到在54行先產出大質數$p$, $q$，並把$n$ release出來
* 隨後進到get_clue function，可以看到他先create一個$d_q$和$d_p$，且$d_p$的range被限制在$(1,\ 2^{20}=1048576)$
* 在28行的地方進入CRT function，這一段是在找一個$d$使其符合中國餘式定理，也就是:
$$
d\ \%\ m=a\\
d\ \%\ n=b
$$
帶入參數就是
$$
d\ \%\ (p-1)=d_p\\
d\ \%\ (q-1)=d_q
$$

## Recon
這一題超難，看了三篇Write Up還是看不懂其中的原理

## Exploit
* Prove of Work
    ```python
    from pwn import *
    from tqdm import trange
    import hashlib

    context.arch = 'amd64'
    # r = process(['python', 'not_my_fault.py'])
    r = remote('mercury.picoctf.net', 41175)

    r.recvuntil(b'Enter a string that starts with "')
    tmp = r.recvline().strip().decode()

    value1 = tmp.split('"')[0]
    value2 = tmp.split(": ")[-1]

    log.info("Prefix = {}, Postfix = {}".format(value1, value2))
    for i in trange(20000000000):
        guess_collision = hashlib.md5((value1 + str(i)).encode()).hexdigest()
        if guess_collision[-6:] == value2:
            r.sendline((value1 + str(i)).encode())
            print("Collision Found: {}".format(value1 + str(i)))
            break

    r.interactive()
    ```
## Reference
[maple3142 - It's Not My Fault 1](https://blog.maple3142.net/2021/03/30/picoctf-2021-writeups/#its-not-my-fault-1)
[It's Not My Fault 1 - Write Up](https://github.com/HHousen/PicoCTF-2021/blob/master/Cryptography/It%27s%20Not%20My%20Fault%201/README.md)
[Attack on CRT-RSA](https://mathoverflow.net/questions/120160/attack-on-crt-rsa/120166?newreg=b5992ec3ffa640ab8587fd12f88332d1)
[picoCTF 2021 It's Not My Fault 1 - Video](https://youtu.be/i7KtIHyHCgE)