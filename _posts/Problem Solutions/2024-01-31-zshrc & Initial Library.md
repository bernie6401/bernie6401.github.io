---
title: "zshrc & Initial Library"
tags: [problem solution]

category: "Problem Solutions"
date: 2024-01-31
---

# zshrc & Initial Library
<!-- more -->

## Zsh
```bash!
$ sudo apt install zsh gawk git -y
$ sudo apt update; sudo apt upgrade -y; sudo apt install curl binutils  vim npm -y
$ chsh -s /bin/zsh
$ curl -sL --proto-redir -all,https https://raw.githubusercontent.com/zplug/installer/master/installer.zsh | zsh
$ vim ~/.zshrc
# Add these lines in .zshrc
# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/sbk6401/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall

# Delete all temp download files
alias ll="ls -al"
find . -name "*:Zone.Identifier" -type f -delete
export ZSH="$HOME/.zplug/repos/robbyrussell/oh-my-zsh"
ZSH_THEME="robbyrussell"
ZSH_THEME="powerlevel10k/powerlevel10k"
source ~/.zplug/init.zsh
npm install -g tldr

# zplug plugins
zplug "romkatv/powerlevel10k", as:theme, depth:1
zplug 'zplug/zplug', hook-build:'zplug --self-manage'
zplug "zsh-users/zsh-autosuggestions"

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
* 客製化 zshrc
    ```bash!
    source ~/anaconda3/bin/activate CTF
    cd /mnt/d/NTU/CTF/PicoCTF/
    alias ll='ls -al'
    alias gccc='gcc -Wl,--dynamic-linker=/usr/src/glibc/glibc_dbg/elf/ld.so -g'
    ```

## gdb-gef
Touch 2 files
```bash
$ wget -O ~/.gdbinit-gef.py -q https://gef.blah.cat/py
$ git clone https://github.com/longld/peda.git ~/peda
$ git clone https://github.com/scwuaptx/Pwngdb.git ~/Pwngdb
$ sudo apt install gdb -y
$ vim ~/.gdbinit
# Add these lines in ~/.gdbinit
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