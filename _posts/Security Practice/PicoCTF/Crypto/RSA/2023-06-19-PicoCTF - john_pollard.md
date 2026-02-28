---
title: PicoCTF - john_pollard
tags: [PicoCTF, CTF, Crypto]

category: "Security Practice｜PicoCTF｜Crypto｜RSA"
date: 2023-06-19
---

# PicoCTF - john_pollard
<!-- more -->
###### tags: `PicoCTF` `CTF` `Crypto`

## Background
[openssl - rsa](https://www.mkssoftware.com/docs/man1/openssl_rsa.1.asp)

## Source code
```
-----BEGIN CERTIFICATE-----
MIIB6zCB1AICMDkwDQYJKoZIhvcNAQECBQAwEjEQMA4GA1UEAxMHUGljb0NURjAe
Fw0xOTA3MDgwNzIxMThaFw0xOTA2MjYxNzM0MzhaMGcxEDAOBgNVBAsTB1BpY29D
VEYxEDAOBgNVBAoTB1BpY29DVEYxEDAOBgNVBAcTB1BpY29DVEYxEDAOBgNVBAgT
B1BpY29DVEYxCzAJBgNVBAYTAlVTMRAwDgYDVQQDEwdQaWNvQ1RGMCIwDQYJKoZI
hvcNAQEBBQADEQAwDgIHEaTUUhKxfwIDAQABMA0GCSqGSIb3DQEBAgUAA4IBAQAH
al1hMsGeBb3rd/Oq+7uDguueopOvDC864hrpdGubgtjv/hrIsph7FtxM2B4rkkyA
eIV708y31HIplCLruxFdspqvfGvLsCynkYfsY70i6I/dOA6l4Qq/NdmkPDx7edqO
T/zK4jhnRafebqJucXFH8Ak+G6ASNRWhKfFZJTWj5CoyTMIutLU9lDiTXng3rDU1
BhXg04ei1jvAf0UrtpeOA6jUyeCLaKDFRbrOm35xI79r28yO8ng1UAzTRclvkORt
b8LMxw7e+vdIntBGqf7T25PLn/MycGPPvNXyIsTzvvY/MXXJHnAqpI5DlqwzbRHz
q16/S1WLvzg4PsElmv1f
-----END CERTIFICATE-----

```

## Recon
* Hint 1: The flag is in the format picoCTF{p,q}
* Hint 2: Try swapping p and q if it does not work
這一題就只是把certificate解出來，發現n超小，所以就直接

## Exploit - openssl
```bash
$ openssl openssl x509 -in cert -pubkey -noout > public.pem
-----BEGIN PUBLIC KEY-----
MCIwDQYJKoZIhvcNAQEBBQADEQAwDgIHEaTUUhKxfwIDAQAB
-----END PUBLIC KEY-----
$ openssl rsa -pubin -in public.pem -text
RSA Public-Key: (53 bit)
Modulus: 4966306421059967 (0x11a4d45212b17f)
Exponent: 65537 (0x10001)
writing RSA key
-----BEGIN PUBLIC KEY-----
MCIwDQYJKoZIhvcNAQEBBQADEQAwDgIHEaTUUhKxfwIDAQAB
-----END PUBLIC KEY-----
```
Use [online tool](https://www.alpertron.com/ECM.HTM) to factor
p = `67867967`
q = `73176001`

Flag: `picoCTF{73176001,67867967}`

## Reference