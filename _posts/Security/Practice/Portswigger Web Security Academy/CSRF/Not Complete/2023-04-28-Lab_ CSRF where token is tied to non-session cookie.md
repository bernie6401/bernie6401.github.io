---
title: 'Lab: CSRF where token is tied to non-session cookie'
tags: [Portswigger Web Security Academy, Web]

category: "Security/Practice/Portswigger Web Security Academy/CSRF/Not Complete"
---

# Lab: CSRF where token is tied to non-session cookie
<!-- more -->
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't fully integrated into the site's session handling system.
* Goal:  To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You have two accounts on the application that you can use to help design your attack. The credentials are as follows:
`wiener:peter`
`carlos:montoya`

* Hint:


## Recon
1. Username: `wiener`
![](https://i.imgur.com/LjQXczA.png)
Session: `XdagGBS9LPa7P1t3m5sxhxNdGNSF567a`
CSRF Key: `liMgrTpwX5psfFRMCHyzuuH6GDT0va5v`
CSRF Token: `ZZYoEyE0OQqp1rvb6XCgs4Uz9us4OCgG`

    Something interesting: when I logout and re-login again, the session changed and the others data are the same
    ![](https://i.imgur.com/npYekP9.png)


2. Username: `carlos`
![](https://i.imgur.com/yxtgtEh.png)
Session: `eblGI5f9PddGlEpYdJvsIUe6chNkLjrd`
CSRF Key: `liMgrTpwX5psfFRMCHyzuuH6GDT0va5v` $\to$ The same with `wiener`
CSRF Token: `ZZYoEyE0OQqp1rvb6XCgs4Uz9us4OCgG` $\to$ The same with `wiener`


## Exp
:::spoiler Success Screenshot

:::

## Reference
[Writeup: CSRF where token is tied to non-session cookie @ PortSwigger Academy](https://medium.com/@frank.leitner/writeup-csrf-where-token-is-tied-to-non-session-cookie-portswigger-academy-60fb8062363b)