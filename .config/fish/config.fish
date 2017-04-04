# ----------------------------------------------------------------------------
# Environment
# ----------------------------------------------------------------------------
xset r rate 250 40
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

# emacs ansi-term support
if test -n "$EMACS"
  set -x TERM eterm-color
end

function fish_title
  true
end

# rbenv
set -gx RBENV_ROOT ~/.rbenv
if test -e $RBENV_ROOT/bin/rbenv
  set -xg PATH ~/.rbenv/bin $PATH
  set -xg PATH ~/.rbenv/shims $PATH
  . (rbenv init -|psub)
end

# haskell
if test -e /Users/sylvain/Library/Haskell/bin
  set -xg PATH /Users/sylvain/Library/Haskell/bin $PATH
end

# go
if test -e /usr/local/go/bin
  set -xg PATH /usr/local/go/bin $PATH
  set -xg GOPATH /Users/sylvain/dev/go $GOPATH
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

# OPAM configuration
if test -e ~/.opam/opam-init/init.fish
  . ~/.opam/opam-init/init.fish > /dev/null 2> /dev/null or true
end

# ----------------------------------------------------------------------------
# vi config
# ----------------------------------------------------------------------------
function fish_mode_prompt; end

function my_fish_key_bindings
  fish_vi_key_bindings
  set fish_bind_mode insert
  bind -M insert -m insert \n execute
  bind \co 'ranger-cd ; fish_prompt'
end
set fish_key_bindings my_fish_key_bindings


# ----------------------------------------------------------------------------
# aliases
# ----------------------------------------------------------------------------
# rr instead of just 'r' since r is already taken by R
alias rr=ranger
alias np=noproxy
# print recent history item backward
alias h='history | tac'

# ----------------------------------------------------------------------------
# Work
# ----------------------------------------------------------------------------
if test -e ~/work/Curbside/config.fish
  . ~/work/Curbside/config.fish
end
