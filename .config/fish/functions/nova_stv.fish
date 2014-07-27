function nova_stv -d "Set the environment for admin access to Openstack labo-stv"
  set -lx ADMIN_TOKEN f0150301-f309-485b-8729-d60411a29a7e
  set -lx OS_USERNAME admin
  set -lx OS_PASSWORD tochange
  set -lx OS_TENANT_NAME admin
  set -lx OS_AUTH_URL http://10.128.56.121:5000/v2.0/
  set -lx OS_REGION_NAME labgns
  noproxy "nova $argv"
end