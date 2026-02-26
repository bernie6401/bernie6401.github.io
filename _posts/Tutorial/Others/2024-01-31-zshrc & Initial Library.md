---
title: "zshrc & Initial Library"
tags: [problem solution]

category: "Tutorial｜Others"
date: 2024-01-31
---

# zshrc & Initial Library
<!-- more -->

## Zsh
```bash
$ sudo apt install zsh gawk git -y
$ sudo apt update; sudo apt upgrade -y; sudo apt install curl binutils  vim npm -y
$ chsh -s /bin/zsh
$ curl -sL --proto-redir -all,https https://raw.githubusercontent.com/zplug/installer/master/installer.zsh | zsh
$ vim ~/.zshrc
```

Add following content in `.zshrc`

```bash
# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
# bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename "/home/sbk6401/.zshrc"
autoload -Uz compinit
compinit
# End of lines added by compinstall


source ~/.zplug/init.zsh

# zplug plugins
zplug "romkatv/powerlevel10k", as:theme, depth:1
zplug "zplug/zplug", hook-build:"zplug --self-manage"
zplug "zsh-users/zsh-autosuggestions"
zplug "zsh-users/zsh-syntax-highlighting", defer:2
zplug "zsh-users/zsh-completions", defer:2

if ! zplug check --verbose; then
        printf "Install? [y/N]: "
        if read -q; then
        
                echo; zplug install
        else
                echo
        fi
fi

zplug load

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
```

客製化 zshrc

```bash
# conda initialize
# !! Contents within this block are managed by "conda init" !!
__conda_setup="$("/home/sbk6401/anaconda3/bin/conda" "shell.zsh" "hook" 2> /dev/null)"
if [ $? -eq 0 ]; then
eval "$__conda_setup"
else
if [ -f "/home/sbk6401/anaconda3/etc/profile.d/conda.sh" ]; then
. "/home/sbk6401/anaconda3/etc/profile.d/conda.sh"
else
export PATH="/home/sbk6401/anaconda3/bin:$PATH"
fi
fi
unset __conda_setup
# end of conda initialize

# Customize your own settings below
conda config --set auto_activate_base false
source ~/anaconda3/bin/activate CTF
cd /mnt/d/CTF-Tools/
alias ll="ls -al"
alias cdctf="cd /mnt/d/CTF/"
alias cdtrash="cd /mnt/d/Downloads/Trash"
alias gccc="gcc -Wl,--dynamic-linker=/usr/src/glibc/glibc_dbg/elf/ld.so -g"
alias cdtool="cd /mnt/d/CTF-Tools/"
alias cleantmp="find . -name '*:Zone.Identifier' -type f -delete" # Delete all temp download files
alias psysh="/mnt/d/CTF-Tools/Web/Language/PHP/psysh"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

export ANDROID_HOME=/mnt/c/Users/berni/AppData/Local/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools
export PATH=$PATH:/usr/local/go/bin
export PATH=$PATH:~/.local/bin
```

## gdb-gef
Touch 2 files
```bash
$ wget -O ~/.gdbinit-gef.py -q https://gef.blah.cat/py
$ git clone https://github.com/longld/peda.git ~/peda
$ git clone https://github.com/scwuaptx/Pwngdb.git ~/Pwngdb
$ sudo apt install gdb -y
$ vim ~/.gdbinit
```

Add following content in `~/.gdbinit`

```bash
set disassembly-flavor intel

define gef
        source ~/.gdbinit-gef.py

        #### gef
        # gef setting
        gef config dereference.max_recursion 2
        gef config context.layout "regs code args source memory stack trace"
        gef config context.nb_lines_backtrace 3
        gef config context.redirect /dev/pts/2
end

define peda
        source ~/peda/peda.py
        source ~/Pwngdb/pwngdb.py
        source ~/Pwngdb/angelheap/gdbinit.py

        define hook-run
        python
import angelheap
angelheap.init_angelheap()
end
        end
end
```

## Reference
* [zsh + zplug快速部屬你的Shell工作環境](https://www.jkg.tw/p2965/)