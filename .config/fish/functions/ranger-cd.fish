function ranger-cd   
  set tempfile '/tmp/chosendir'
  /usr/local/bin/ranger --choosedir=$tempfile (pwd)
  if test -f $tempfile
      if [ (cat $tempfile) != (pwd) ]
        cd (cat $tempfile)
      end
  end
  rm -f $tempfile
end
