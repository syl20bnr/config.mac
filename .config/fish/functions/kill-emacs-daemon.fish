function kill-emacs-daemon
  for pid in ( ps aux | grep "emacs --daemon" | grep -v "grep" | awk '{print $2}' )
    command kill -9 $pid
  end
end




