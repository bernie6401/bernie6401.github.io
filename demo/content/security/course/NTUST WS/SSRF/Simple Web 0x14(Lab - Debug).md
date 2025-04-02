---
title: Simple Web 0x14(Lab - Debug)
tags: [NTUSTWS, CTF, Web]

---

# Simple Web 0x14(Lab - Debug)
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:9020/

## Background

## Source code
:::spoiler source code
```python=
from flask import Flask, request, Response
import urllib.request
import json

app = Flask(__name__)

app.config['FLAG'] = "FL4G{fake_flag}"

@app.route('/')
def index():
    return '''
<form action="/proxy">
    <input type="text" name="url" placeholder="URL">
    <input type="submit">
</form>
<p><a href="/source">Source Code</a> | <a href="/debug">Debug</a></p>
'''

@app.route("/proxy")
def proxy():
    url = request.args.get("url")
    if url is None:
        return "No URL provided"
    if "https://" not in url:
        url = "https://" + url
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        return str(e)

@app.route("/debug")
def debug():
    # only allow access for localhost
    if request.remote_addr != "127.0.0.1":
        return "Access denied", 403
    return json.dumps(app.config, default=lambda _: None)

@app.route("/source")
def source():
    import re
    source_code = open(__file__).read()
    source_code = re.sub(r'FLAG{.*}', r'FL4G{fake_flag}', source_code, count=1)
    return Response(source_code, mimetype='text/plain')
```
:::
### Analyze
* `/index` page
It has a blank that can type arbitrary URL and it'll send to `/proxy` route page to verify.
* `/proxy` page
It'll add `https://` if the URL has no the string
* <font color="FF0000">`/debug` page</font>
If the request URL is not `127.0.0.1` then it'll forbidden the request, otherwise, it'll print the configuration with json type
hint: it has loaded the flag in app configuration already, so we just tried to use `SSRF` to access to `/debug`.

## Exploit - SSRF
We need to bypass `https://` constraint and add in our URL like below.
Payload: `http://127.0.0.1/debug?https://`