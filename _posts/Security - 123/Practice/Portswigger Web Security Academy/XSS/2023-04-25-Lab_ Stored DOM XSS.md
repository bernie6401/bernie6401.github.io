---
title: 'Lab: Stored DOM XSS'
tags: [Portswigger Web Security Academy, Web]

category: "Security/Practice/Portswigger Web Security Academy/XSS"
---

# Lab: Stored DOM XSS
<!-- more -->
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab demonstrates a stored DOM vulnerability in the blog comment functionality.
* Goal: To solve this lab, exploit this vulnerability to call the `alert()` function.

## Recon
1. Find the injected place
According to the description, we know that the comment place of each post has some problems. So, we can try to inject something.
2. Try to inject
Comment Payload: `<script>alert(123)</script>`
![](https://i.imgur.com/JF1oEdx.png)
Seems weird, and when you browse the page source, you'll find out that it calls external `js` files to import the comment, i.e.:
![](https://i.imgur.com/1EOREIf.png)
![](https://i.imgur.com/BCeovon.png)

3. What is `loadCommentsWithVulnerableEscapeHtml.js`
The main purpose of this file is to load the comment into the page and filter some sensitive characters.
    :::spoiler A part of source code
    ```javascript!
    ...
    function escapeHTML(html) {return html.replace('<', '&lt;').replace('>', '&gt;');}
    ...
    ```
    :::
    However...
    :::danger
    According to [JavaScript Document](https://developer.mozilla.org/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/String/replace)
    ![](https://i.imgur.com/KgJD2oy.png)
    :::
4. Try to inject more `<>` char
Comment Payload: `<><script>alert(123)</script>`
![](https://i.imgur.com/Rs7A0tc.png)

![](https://i.imgur.com/KKyKuie.png)

Seems it can be injected but can not be rendered properly because the comments are loaded from external space. So, we could change our payload to `img` tag.

## Exp
New Comment Payload: `<><img src="a" onerror="alert(123)">`
![](https://i.imgur.com/eONdVV6.png)

:::spoiler Success Screenshot
![](https://i.imgur.com/DBHEhM3.png)
:::

## Reference