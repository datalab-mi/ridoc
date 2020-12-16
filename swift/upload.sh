#!/bin/sh

# first argument is container name
# second is object
# third, choose swift or curl

[ -z "${OS_AUTH_TOKEN}" -o -z "${OS_STORAGE_URL}" ] && echo "missing auth variables"

echo "$(dirname $2)"
#--object-name "$(basename $1)"
if [ $3 = "swift" ]
then
  # with SWIFT, support folder
  swift --debug \
   --os-storage-url "${OS_STORAGE_URL}/$1" --os-auth-token "${OS_AUTH_TOKEN}" \
   upload $2

elif [ $3 = "curl" ]
then
  # with CURL, only file. Need eventually to loop over a folder
  echo 'curl -k -i -T $2\
      ${OS_STORAGE_URL}/$1/$2 \
      -X PUT \
      -H "X-Auth-Token: ${OS_AUTH_TOKEN}" -vv'

  curl -k -i -T $2\
      "${OS_STORAGE_URL}/$1/$2" \
      -X PUT \
      -H "X-Auth-Token: ${OS_AUTH_TOKEN}" -vv

else
  echo "Choose swift or curl"
fi

# https://docs.openstack.org/api-ref/object-store/?expanded=create-or-replace-object-detail,create-or-update-object-metadata-detail
# Help: http://doc.swift.surfsara.nl/en/latest/Pages/Clients/curl.html
