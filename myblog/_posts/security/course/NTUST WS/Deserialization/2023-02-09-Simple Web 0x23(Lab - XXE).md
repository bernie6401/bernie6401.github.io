---
title: Simple Web 0x23(Lab - XXE)
tags: [NTUSTWS, CTF, Web]

---

# Simple Web 0x23(Lab - XXE)
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8604/

## Background
[XML Tree](https://www.w3schools.com/xml/xml_tree.asp)
[XML Parser](https://www.w3schools.com/xml/xml_parser.asp)
[AJAX - Server Response](https://www.w3schools.com/xml/ajax_xmlhttprequest_response.asp)
[XML DTD](https://www.w3schools.com/xml/xml_dtd.asp)

[输入流 php://input](https://phper.shujuwajue.com/shu-zu/shu-ru-liu-php-input)
> php://input可以读取没有处理过的POST数据。

[Day 18：Stream 概述](https://ithelp.ithome.com.tw/articles/10217536)
> php://input
    取得所有的 input 通常來源於 HTTP body，值得注意的是，由這個 Stream 取得的內容是 Raw Body，所以需要自行解析。
    
[來自外部的威脅-XXE漏洞攻擊成因](https://www.digicentre.com.tw/industry_detail?id=38)
:::spoiler XXE course lecture
![](https://i.imgur.com/NsyIcdt.png)

![](https://i.imgur.com/zYonfqc.png)
:::
:::spoiler exploit type
![](https://i.imgur.com/IJlFonF.png)

![](https://i.imgur.com/N9VNyBC.png)

![](https://i.imgur.com/uqPwH5H.png)

![](https://i.imgur.com/j8WI9eQ.png)
:::
## Source code
```php=
<?php
   $xmlfile = urldecode(file_get_contents('php://input'));
   if (!$xmlfile) die(show_source(__FILE__));

   $dom = new DOMDocument();
   $dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
   $creds = simplexml_import_dom($dom);
   $user = $creds->user;
   echo "You have logged in as user $user";
?>
```
## Exploit - XXE
1. Normal Usage in this webpage


## Reference