# ----------------------------------------------------------------------------
# oh-my-fish config
# ----------------------------------------------------------------------------
set fish_path ~/.oh-my-fish
set fish_theme syl20bnr

# Load oh-my-fish configuration.
. $fish_path/oh-my-fish.fish

function my_fish_key_bindings
  fish_vi_key_bindings
  set fish_bind_mode default
  bind -M insert -m default \n execute
  bind \co 'ranger-cd ; fish_prompt'  
end
set fish_key_bindings my_fish_key_bindings
xset r rate 250 40

# ----------------------------------------------------------------------------
# Environment
# ----------------------------------------------------------------------------
set fish_greeting

# use emacs for fast file lookup (using emacs daemon)
set -x ALTERNATE_EDITOR ""
set -x EDITOR et

# force fish as the current shell in case of a different default shell
set -x SHELL /usr/local/bin/fish

# tmux
if test -z "$TMUX"
  set -x TERM xterm-256color
end

# for mac port
set -xg PATH /opt/local/bin /opt/local/sbin $PATH

# rbenv
set -gx RBENV_ROOT ~/.rbenv
if test -e $RBENV_ROOT/bin/rbenv
  set -xg PATH ~/.rbenv/bin $PATH
  set -xg PATH ~/.rbenv/shims $PATH
  . (rbenv init -|psub)
end

# force english language
set -x LC_ALL en_GB.UTF-8

# java home
# /usr/libexec/java_home allows to select easily the version
# of java installed on the system
# to force a specific version:
# /usr/libexec/java_home -v 1.6
# to list the available versions:
# /usr/libexec/java_home -V
set -x JAVA_HOME (/usr/libexec/java_home)

# ----------------------------------------------------------------------------
# aliases
# ----------------------------------------------------------------------------
# rr instead of just 'r' since r is already taken by R
alias rr=ranger
alias np=noproxy
# print recent history item backward
alias h='history | tac'
