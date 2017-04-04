# Minimal resource file just to be able to launch fish
# I keep bash as the default shell to make Emacs happy :-)
if [ -z "$EMACS" ]; then
  export TERM=xterm-256color
else
  export TERM=eterm-color
fi
export PATH=/usr/local/bin\
       :/usr/local/sbin\
       :/bin\
       :/usr/bin\
       :/Users/sylvain/Library/Haskell/bin\
       :/usr/local/go/bin\
       :/Users/sylvain/.i3ci/bin\
       :${PATH}
# go
export GOPATH=/Users/sylvain/dev/go
# for pdf-tools
export PKG_CONFIG_PATH=/usr/local/Cellar/zlib/1.2.8/lib/pkgconfig:/usr/local/lib/pkgconfig:/opt/X11/lib/pkgconfig
# java 1.8
export JAVA_HOME=`/usr/libexec/java_home -v 1.8`

# Set keyboard repeat delay and rate
xset r rate 250 40

alias f='fish'

cd ~
