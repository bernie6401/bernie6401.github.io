---
title: PicoCTF - ARMssembly 0
tags: [PicoCTF, CTF, Reverse]

category: "Security Practice｜PicoCTF｜Reverse"
date: 2024-01-31
---

# PicoCTF - ARMssembly 0
<!-- more -->

## Source code
:::spoiler ARM assembly code
```
	.arch armv8-a
	.file	"chall.c"
	.text
	.align	2
	.global	func1
	.type	func1, %function
func1:
	sub	sp, sp, #16
	str	w0, [sp, 12]
	str	w1, [sp, 8]
	ldr	w1, [sp, 12]
	ldr	w0, [sp, 8]
	cmp	w1, w0
	bls	.L2
	ldr	w0, [sp, 12]
	b	.L3
.L2:
	ldr	w0, [sp, 8]
.L3:
	add	sp, sp, 16
	ret
	.size	func1, .-func1
	.section	.rodata
	.align	3
.LC0:
	.string	"Result: %ld\n"
	.text
	.align	2
	.global	main
	.type	main, %function
main:
	stp	x29, x30, [sp, -48]!
	add	x29, sp, 0
	str	x19, [sp, 16]
	str	w0, [x29, 44]
	str	x1, [x29, 32]
	ldr	x0, [x29, 32]
	add	x0, x0, 8
	ldr	x0, [x0]
	bl	atoi
	mov	w19, w0
	ldr	x0, [x29, 32]
	add	x0, x0, 16
	ldr	x0, [x0]
	bl	atoi
	mov	w1, w0
	mov	w0, w19
	bl	func1
	mov	w1, w0
	adrp	x0, .LC0
	add	x0, x0, :lo12:.LC0
	bl	printf
	mov	w0, 0
	ldr	x19, [sp, 16]
	ldp	x29, x30, [sp], 48
	ret
	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits

```
:::

## Recon
這一題是ARM架構的組語，真的懶得看，想說可以先compile完之後用IDA看一下psudo code，但search半天都找不到如何compile，compile完的東西還不能執行，要瘋了，所幸最後有找到repo的相關資料[^compile_arm_file]

## Exploit
```bash
$ sudo apt install gcc-aarch64-linux-gnu -y
$ sudo apt install binutils-aarch64-linux-gnu -y
$ aarch64-linux-gnu-as -o a.o [the name of your source file]
$ aarch64-linux-gnu-gcc -static -o [the name of the executable] a.o
```
再用IDA反編譯就完事了

## Reference
[^compile_arm_file]:[Running ARMv8 via Linux Command Line](https://github.com/joebobmiles/ARMv8ViaLinuxCommandline)