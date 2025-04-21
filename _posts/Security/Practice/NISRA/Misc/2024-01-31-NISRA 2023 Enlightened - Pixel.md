---
title: NISRA 2023 Enlightened - Pixel
tags: [NISRA, CTF, Misc]

category: "Security/Practice/NISRA/Misc"
---

# NISRA 2023 Enlightened - Pixel
<!-- more -->

## Source Code
![](https://hackmd.io/_uploads/HkF8f_702.png)

## Recon
這一題真的很難，應該說有想過，不過很麻煩就是了，每一個色塊都有一組RGB的數值，然後只要把它轉換成ASCII，再把每一個字元串起來，就會是一組base64的code，轉換之後就拿到一組ciphertext，接著就丟到cyberchef看看一般的工具可不可以解，最後是用rot13解出來，除了最一開始的地方需要一點通靈之外，其他都很簡單，但...寫script頗麻煩

## Exploit
```python
from PIL import Image
from base64 import b64decode

img = Image.open("./NISRA-Enlightened-2023/Misc/Final-Pixel.png")

pixels = []
for row in range(8):	# 8 rows
	for col in range(8):	# 8 columns
		r, g, b = img.getpixel((row * 64 + 1, col * 64 + 1))	# each grid: 64 x 64
		if r == 255 and g == 255 and b == 255:
			break
		else:
			pixels.append((chr(r), chr(g), chr(b)))
	if r == 255 and g == 255 and b == 255:
		break

flag = ""
print(pixels)
for r, g, b in pixels:
	flag += r + g + b
print(flag)
print(b64decode(flag.encode()))
```
```bash!
$ python exp.py
[('c', '3', 'l'), ('u', 'd', 'D'), ('o', 'g', 'Q'), ('V', 'Z', 'G'), ('R', 'U', '5'), ('7', 'T', 'l'), ('9', 'l', 'T'), ('m', 'Y', '3'), ('U', 'k', 'V'), ('f', 'N', 'k'), ('U', '0', 'Q'), ('1', 'U', 'x'), ('U', 'F', '9'), ('l', 'U', 'm'), ('N', 'F', 'U'), ('m', 'Z', 'S'), ('Q', 'W', 'c'), ('k', 'X', '0'), ('5', 'f', 'R'), ('2', 'o', 'w'), ('L', 'V', 'E'), ('x', 'W', 'j'), ('N', 'h', 'Z'), ('j', 'E', 'w'), ('Y', 'T', 'Q'), ('x', 'X', '2'), ('N', '2', 'c'), ('G', 'd', 'o'), ('R', 'X', 'J'), ('f', 'T', 'm'), ('Z', 'f', 'N'), ('F', '9', 'l'), ('U', 'n', 'B'), ('H', 'b', 'm'), ('E', '2', 'S'), ('D', 'F', 'O'), ('R', 'V', '9'), ('a', 'b', 'j'), ('d', 'l', 'd'), ('m', 't', 'f'), ('Y', 'm', 'V'), ('f', 'd', 'G'), ('V', 'W', 'c'), ('V', '9', 'i'), ('U', '1', '9'), ('G', 'Z', 'E'), ('h', 'A', 'Z'), ('V', 'J', 'f'), ('Q', '1', 'Z'), ('L', 'c', 'n'), ('l', 'm', 'f'), ('Q', '=', '=')]
c3ludDogQVZGRU57Tl9lTmY3UkVfNkU0Q1UxUF9lUmNFUmZSQWckX05fR2owLVExWjNhZjEwYTQxX2N2cGdoRXJfTmZfNF9lUnBHbmE2SDFORV9abjdldmtfYmVfdGVWcV9iU19GZEhAZVJfQ1ZLcnlmfQ==
b'synt: AVFEN{N_eNf7RE_6E4CU1P_eRcERfRAg$_N_Gj0-Q1Z3af10a41_cvpghEr_Nf_4_eRpGna6H1NE_Zn7evk_be_teVq_bS_FdH@eR_CVKryf}'
```

Flag: `NISRA{A_rAs7ER_6R4PH1C_rEpREsENt$_A_Tw0-D1M3ns10n41_pictuRe_As_4_rEcTan6U1AR_Ma7rix_or_grId_oF_SqU@rE_PIXels}`

## Reference
[NISRA - Final WP](https://hackmd.io/@nisra/BJsuIwCT2)