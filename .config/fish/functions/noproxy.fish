function noproxy -S -d "Call a command without any proxy"
  set -l back_http_proxy "$http_proxy"
  set -l back_https_proxy "$https_proxy"
  set -x http_proxy
  set -x https_proxy
  eval $argv
  set -x http_proxy "$back_http_proxy"
  set -x https_proxy "$back_httpsd_proxy"
end