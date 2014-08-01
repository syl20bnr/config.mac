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

# ----------------------------------------------------------------------------
# aliases
# ----------------------------------------------------------------------------
# rr instead of just 'r' since r is already taken by R
alias rr=ranger
alias np=noproxy
# force english language for git
alias git='env LC_ALL=en_US git'
# print recent history item backward
alias history='history | tac'
