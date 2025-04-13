---
title: A&D of Network Security - Lab 12
tags: [NTU, NTU_PADNS]

category: "Security/Course/NTU PADNS"
---

# A&D of Network Security - Lab 12
###### tags: `Practicum of A&D of NS` `NTU`

## Video
[NTU PADNS Lecture 12](https://files-1.dlc.ntu.edu.tw/cool-video/202305/c6cc49a9-e1f9-4a9e-a7dc-70c4f79c98b1/transcoded.mp4?AWSAccessKeyId=C6ueMrUe5JyPkWQJAyKp&Expires=1684429335&Signature=UQaLvueX0U%2Bvs65WhFgrks9vg%2Fc%3D)

## Background
[What is _mbscmp?](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/strcmp-wcscmp-mbscmp?view=msvc-170)
```clike!
int _mbscmp(
   const unsigned char *string1,
   const unsigned char *string2
);
```
Return Value
> <0 	string1 is less than string2
> =0 	string1 is identical to string2
> \>0 	string1 is greater than string2


## Recon

### Static - IDA Pro
:::spoiler Main Source Code
```clike=
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4; // [esp+10h] [ebp-181Ch]
  char v5; // [esp+410h] [ebp-141Ch]
  char v6; // [esp+810h] [ebp-101Ch]
  char v7; // [esp+C10h] [ebp-C1Ch]
  CHAR v8; // [esp+1024h] [ebp-808h]
  CHAR ServiceName; // [esp+1428h] [ebp-404h]
  const char *v10; // [esp+1828h] [ebp-4h]

  if ( argc == 1 )
  {
    if ( !sub_401000() )
      sub_402410();
    sub_402360();
  }
  else
  {
    v10 = argv[argc - 1];
    if ( !sub_402510(v10) )
      sub_402410();
    if ( _mbscmp((const unsigned __int8 *)argv[1], &byte_40C170) )
    {
      if ( _mbscmp((const unsigned __int8 *)argv[1], &byte_40C16C) )
      {
        if ( _mbscmp((const unsigned __int8 *)argv[1], &byte_40C168) )
        {
          if ( _mbscmp((const unsigned __int8 *)argv[1], aCc) )
            sub_402410();
          if ( argc != 3 )
            sub_402410();
          if ( !sub_401280(&v5, 1024, &v6, 1024, &v4, 1024, &v7) )
            sub_402E7E(aKSHSPSPerS, &v5);
        }
        else
        {
          if ( argc != 7 )
            sub_402410();
          sub_401070(argv[2], argv[3], argv[4], argv[5]);
        }
      }
      else if ( argc == 3 )
      {
        if ( sub_4025B0(&v8) )
          return -1;
        sub_402900(&v8);
      }
      else
      {
        if ( argc != 4 )
          sub_402410();
        sub_402900(argv[2]);
      }
    }
    else if ( argc == 3 )
    {
      if ( sub_4025B0(&ServiceName) )
        return -1;
      sub_402600(&ServiceName);
    }
    else
    {
      if ( argc != 4 )
        sub_402410();
      sub_402600(argv[2]);
    }
  }
  return 0;
}
```
:::

* If we execute it directly, nothing happened.

## Lab 9-1 Questions
1. How can you get this malware to install itself?
Ans: You can get the program to install itself by providing it with the `-in` option, along with the password. Alternatively, you can patch the binary to skip the password verification check.
    ![](https://hackmd.io/_uploads/HJvh2Xdr2.png)

2. What are the command-line options for this program? What is the password requirement?
Ans: The command-line options for the program are one of four values and the password. The password is the string `abcd` and is required for all actions except the default behavior. The -in option instructs the malware to install itself. The `-re` option instructs the malware to remove itself. The `-c` option instructs the malware to update its configuration, including its beacon IP address. The `-cc` option instructs the malware to print its current configuration to the console. By default, this malware functions as a backdoor if installed.
3. How can you use `OllyDbg` to permanently patch this malware, so that it doesn’t require the special command-line password?
Ans: You can patch the binary by changing the first bytes of the function at address 0x402510 to always return true. The assembly instruction for this behavior is `MOV EAX, 0x1; RETN;`, which corresponds to the byte sequence `B8 01 00 00 00 C3`.
4. What are the host-based indicators of this malware?
Ans: The malware creates the registry key HKLM\Software\Microsoft \XPS\ Configuration (note the trailing space after Microsoft). The malware also creates the service XYZ Manager Service, where XYZ can be a parameter provided at install time or the name of the malware executable. Finally, when the malware copies itself into the Windows System directory, it may change the filename to match the service name.
5. What are the different actions this malware can be instructed to take via the network?
Ans: The malware can be instructed to execute one of five commands via the network: SLEEP, UPLOAD, DOWNLOAD, CMD, or NOTHING. The SLEEP command instructs the malware to perform no action for a given period of time. The UPLOAD command reads a file from the network and writes it to the local system at a specified path. The DOWNLOAD command instructs the malware to send the contents of a local file over the network to the remote host. The CMD command causes the malware to execute a shell command on the local system. The NOTHING command is a no-op command that causes the malware to do nothing.
6. Are there any useful network-based signatures for this malware?
Ans: By default, the malware beacons http://www.practicalmalwareanalysis.com/ ; however, this is configurable. The beacons are HTTP/1.0 GET requests for resources in the form xxxx/xxxx.xxx, where x is a random alphanumeric ASCII character. The malware does not provide any HTTP headers with its requests

## Lab 9-2 Questions
1. What strings do you see statically in the binary?
Ans: The imports and the string cmd are the only interesting strings that appear statically in the binary.
2. What happens when you run this binary? 
Ans: It terminates without doing much.
3. How can you get this sample to run its malicious payload? 
Ans: Rename the file *ocl.exe* before you run it.
4. What is happening at 0x00401133?
Ans: A string is being built on the stack, which is used by attackers to obfuscate strings from simple strings utilities and basic static analysis techniques.
5. What arguments are being passed to subroutine 0x00401089? 
Ans: The string 1qaz2wsx3edc and a pointer to a buffer of data are passed to subroutine 0x401089.
6. What domain name does this malware use?
Ans: The malware uses the domain `practicalmalwareanalysis.com`.
7. What encoding routine is being used to obfuscate the domain name?
Ans: The malware will XOR the encoded DNS name with the string 1qaz2wsx3edc to decode the domain name.
8. What is the significance of the `CreateProcessA` call at 0x0040106E?
Ans: The malware is setting the `stdout`, `stderr`, and `stdin` handles (used in the `STARTUPINFO` structure of `CreateProcessA`) to the socket. Since `CreateProcessA` is called with cmd as an argument, this will create a reverse shell by tying the command shell to the socket.

## Reference
[Lab 9-1](https://www.cnblogs.com/houhaibushihai/p/10310324.html)
[恶意代码分析实战 Lab 9-1 习题笔记](https://blog.csdn.net/isinstance/article/details/78520494)
[恶意代码分析实战 Lab 9-2 习题笔记](https://blog.csdn.net/isinstance/article/details/78841910)