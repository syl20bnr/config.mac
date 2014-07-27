#!/bin/bash
# Starts emacs client in a terminal.
# It will start the emacs daemon if it is not already started.
# test required for compatibility with ranger
if [ "$1" = "--" ]; then
  emacsclient -nw -c "${@:2}" -a ""
else
  emacsclient -nw -c "${@:1}" -a ""
fi
