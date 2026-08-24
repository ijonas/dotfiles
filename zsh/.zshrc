

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# You can also set it to another string to have that shown instead of the default red dots.
# e.g. COMPLETION_WAITING_DOTS="%F{yellow}waiting...%f"
# Caution: this setting can cause issues with multiline prompts in zsh < 5.7.1 (see #5765)
COMPLETION_WAITING_DOTS="true"

# Oh My Zsh is installed by bin/install. Keep startup usable when it is absent.
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME=""
plugins=(git)
if [[ -r "$ZSH/oh-my-zsh.sh" ]]; then
    source "$ZSH/oh-my-zsh.sh"
fi

# User configuration

HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt SHARE_HISTORY

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi
export EDITOR="nvim"

if [[ -e ~/.secret-env ]]; then
    source ~/.secret-env
fi

if [[ -e ~/dotfiles/pyenv ]]; then
    source ~/dotfiles/pyenv
fi
if [[ -e ~/.aliases ]]; then
    source ~/.aliases
fi
if [[ -e ~/dotfiles/nvm ]]; then
    source ~/dotfiles/nvm
fi
if [[ -e ~/dotfiles/julia ]]; then
    source ~/dotfiles/julia
fi
if [[ -e ~/dotfiles/golang ]]; then
    source ~/dotfiles/golang
fi
if [[ -e ~/dotfiles/path ]]; then
    source ~/dotfiles/path
fi
if [[ -e ~/dotfiles/k0s ]]; then
    source ~/dotfiles/k0s
fi
if [[ -e ~/dotfiles/aws ]]; then
    source ~/dotfiles/aws
fi

if command -v starship >/dev/null 2>&1; then
    eval "$(starship init zsh)"
fi

# Added by Windsurf - Next
export PATH="/Users/ijonas/.codeium/windsurf/bin:$PATH"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# bun completions
[ -s "/Users/ijonas/.bun/_bun" ] && source "/Users/ijonas/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# opencode
export PATH=/home/ijonas/.opencode/bin:$PATH

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/home/ijonas/proj/shapeshifters/google-cloud-sdk/path.zsh.inc' ]; then . '/home/ijonas/proj/shapeshifters/google-cloud-sdk/path.zsh.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/home/ijonas/proj/shapeshifters/google-cloud-sdk/completion.zsh.inc' ]; then . '/home/ijonas/proj/shapeshifters/google-cloud-sdk/completion.zsh.inc'; fi


export JAVA_HOME=/opt/android-studio/jbr
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$JAVA_HOME/bin:$PATH:$ANDROID_HOME/platform-tools
