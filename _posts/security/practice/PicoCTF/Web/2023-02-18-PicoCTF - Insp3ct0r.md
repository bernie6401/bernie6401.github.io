---
title: PicoCTF - Insp3ct0r
tags: [PicoCTF, CTF, Web]

category: "Security/Practice/PicoCTF/Web"
---

# PicoCTF - Insp3ct0r
<!-- more -->
###### tags: `PicoCTF` `CTF` `Web`
Challenge: [Insp3ct0r](http://jupiter.challenges.picoctf.org:9670/)

## Source code

## Exploit - Browser Inspector
HTML
```html!
<!doctype html>
<html>
  <head>
    <title>My First Website :)</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans|Roboto" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="mycss.css">
    <script type="application/javascript" src="myjs.js"></script>
  </head>

  <body>
    <div class="container">
      <header>
	<h1>Inspect Me</h1>
      </header>

      <button class="tablink" onclick="openTab('tabintro', this, '#222')" id="defaultOpen">What</button>
      <button class="tablink" onclick="openTab('tababout', this, '#222')">How</button>
      
      <div id="tabintro" class="tabcontent">
	<h3>What</h3>
	<p>I made a website</p>
      </div>

      <div id="tababout" class="tabcontent">
	<h3>How</h3>
	<p>I used these to make this site: <br/>
	  HTML <br/>
	  CSS <br/>
	  JS (JavaScript)
	</p>
	<!-- Html is neat. Anyways have 1/3 of the flag: picoCTF{tru3_d3 -->
      </div>
      
    </div>
    
  </body>
</html>
```
CSS
Download it and search specific string
```bash!
$ strings mycss.css | grep "flag"
/* You need CSS to make pretty pages. Here's part 2/3 of the flag: t3ct1ve_0r_ju5t */
```
Javascript
![](https://i.imgur.com/8SLLNHC.png)

* Combine the fragment flag: `picoCTF{tru3_d3t3ct1ve_0r_ju5t_lucky?2e7b23e3}`