#!/bin/bash
# Starts emacs client with a GUI.
# It will start the emacs daemon if it is not.
emacsclient -a "" -c ${@:1}
