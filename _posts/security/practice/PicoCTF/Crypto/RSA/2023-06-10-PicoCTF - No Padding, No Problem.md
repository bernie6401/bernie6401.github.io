---
title: 'PicoCTF - No Padding, No Problem'
tags: [PicoCTF, CTF, Crypto]

category: "Security > Practice > PicoCTF > Crypto > RSA"
---

# PicoCTF - No Padding, No Problem
###### tags: `PicoCTF` `CTF` `Crypto`

## Description
Oracles can be your best friend, they will decrypt anything, except the flag's ciphertext. How will you break it? Connect with nc mercury.picoctf.net 10333.

## Hint
What can you do with a different pair of ciphertext and plaintext? What if it is not so different after all...


## Recon
We can try to decrypt ciphertext directly.
```bash
ciphertext: 1969221237575652521155717732207422245260989124462636800279815175985091279976278420735388546000111469136091964900122438057245980826047478280799307045156672217664430153262319375993342808217618594292553441397334562535792273632256157246548036534684500140935101268806406561259397100648254721771966657212392193037


Give me ciphertext to decrypt: 1969221237575652521155717732207422245260989124462636800279815175985091279976278420735388546000111469136091964900122438057245980826047478280799307045156672217664430153262319375993342808217618594292553441397334562535792273632256157246548036534684500140935101268806406561259397100648254721771966657212392193037
Will not decrypt the ciphertext. Try Again
```

## Exploit
We know that $Enc(m_1) * Enc(m_2) = ((m_1^e) * (m_2^e))\ mod\ n = (m_1 * m_2)^e\ mod\ n = Enc(m_1 * m_2)$
$$
c' = 2^e\ (mod\ n)*c \\
\begin{align}
m' &= {c'}^d\ (mod\ n) \\
&= 2^{ed}*c^d\ (mod\ n) \\
&= 2 * c^d\ (mod\ n) \\
\end{align}\\
m = m' // 2
$$
```python
from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
import binascii


context.arch = 'amd64'
r = remote("mercury.picoctf.net", 10333)

for i in range(4):
    r.recvline()

n = int(str(r.recvline().strip().decode()).split(" ")[-1])
e = int(str(r.recvline().strip().decode()).split(" ")[-1])
c = int(str(r.recvline().strip().decode()).split(" ")[-1])

log.info(f"n = {n}\ne = {e}\nc = {c}")

m = b'2'
# r.sendline(long_to_bytes(pow(bytes_to_long(m), e, n)))
r.recvuntil(b"Give me ciphertext to decrypt: ")
r.sendline(str(pow(2, e, n) * c).encode())
response = int(str(r.recvline().strip().decode()).split(" ")[-1])
plaintext = response // 2
print(binascii.unhexlify("{:x}".format(plaintext)))

r.close()
```

## Reference
[picoCTF No Padding, No Problem](https://youtu.be/iFpLqVoFR08)