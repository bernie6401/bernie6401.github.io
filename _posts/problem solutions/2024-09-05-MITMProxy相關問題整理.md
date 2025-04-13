---
title: MITMProxy相關問題整理
tags: [problem solution]

category: "Problem Solutions"
---

# MITMProxy相關問題整理
<!-- more -->
資料來源: https://github.com/mitmproxy/mitmproxy/issues/5442

## Server TLS handshake failed. The remote server does not speak TLS.
代表連線的標的無法處理https的scheme，如果確定連線的目標是開在localhost或是一定是http scheme的話，可以利用script去hook流量把https改掉
```python!
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # 檢查請求是否是 HTTPS
    if flow.request.scheme == "https":
        # 將 URL 中的 HTTPS 替換為 HTTP
        flow.request.url = flow.request.url.replace('https://', 'http://')
```

## Unable to establish TLS connection with server (The remote server does not speak TLS.). Trying to establish TLS with client anyway. If you plan to redirect requests away from this server, consider setting `connection_strategy` to `lazy` to suppress early connections.
出現這個warning，