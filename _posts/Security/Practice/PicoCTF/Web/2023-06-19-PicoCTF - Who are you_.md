---
title: PicoCTF - Who are you?
tags: [PicoCTF, CTF, Web]

category: "Security｜Practice｜PicoCTF｜Web"
date: 2023-06-19
---

# PicoCTF - Who are you?
<!-- more -->
###### tags: `PicoCTF` `CTF` `Web`

## Background

### [【Chrome 85 更新】淺談 Referer-Policy 和更新影響](https://www.maxlist.xyz/2020/08/03/chrome-85-referer-policy/)
> ### HTTP Referer 是什麼?
>
>當使用者訪問網站時，會發送請求 (request) 給伺服器主機，而請求 header 中會有一個欄位是「referer」，而此欄位會存放當前請求來源的位置，也就是說請求的來源頁面。
>
>舉個例子：當小明從「iT邦幫忙」網站中點擊連結後，進入「Max 行銷誌」網站時，所發送的 request 請求 referer 就會是 https://ithelp.ithome.com.tw/ 的網址。

### [RFC 2616 - Date](https://datatracker.ietf.org/doc/html/rfc2616#section-14.18)
> The Date general-header field represents the date and time at which
   the message was originated, having the same semantics as orig-date in
   RFC 822. The field value is an HTTP-date, as described in section
   3.3.1; it MUST be sent in RFC 1123 [8]-date format.
>
>       Date  = "Date" ":" HTTP-date
>
>   An example is
>
>       Date: Tue, 15 Nov 1994 08:12:31 GMT

### [HTTP headers | DNT](https://www.geeksforgeeks.org/http-headers-dnt/)
> The HTTP DNT Header is a request header that allows users to choose if their activity could be tracked by each server and web application that they communicate with via HTTP. The generated header field is a mechanism that allows the user to opt-in or out of the tracking. Tracking allows user to experience personalized content on web. The option to opt-out of tracking was created with growing privacy demands among users.
> Syntax:
>
>     DNT:0
>     DNT:1
> Directives :
>
>
> The following field value is generated for HTTP DNT header field if the tracking preference is set as enabled
>
>   * 1: This directive indicates that user prohibits tracking at the target site.
>   * 0: This directive indicates that user allows tracking on or the user has granted an exception at the given target site.



## Recon
雖然這一題是for beginner但是想了超級無敵久還是不知道在考啥，因此也是只能拜讀別人的WP然後在印度口音的薰陶下找到解答，簡單來說就是考packet的header而已

## Exploit - Header<font color="FF0000">通靈</font>
1. Only people who use the official PicoBrowser are allowed on this site!
改`User-Agent`成`PicoBrowser`
2. I don't trust users visiting from another site
新增`Referer: mercury.picoctf.net:34588`
3. Sorry, this site only worked in 2018
新增`Date: Tue, 15 Nov 2018 08:12:31 GMT`
4. I don't trust users who can be tracked
新增`DNT: 1`
5. This website is only for people frome Sweden
上網搜尋一下Sweden的IP然後新增`X-Forwarded-For: 109.75.224.255`
6. You're in Sweden but you don't speak Swedish
上網搜尋Sweden Accept-Language然後新增`Accept-Language: sv-SE`就拿到flag了

Flag: `picoCTF{http_h34d3rs_v3ry_c0Ol_much_w0w_79e451a7}`
 
## Reference
[who are you?? | PicoCTF | CTF for beginners](https://youtu.be/SkwmVZB5FGI)