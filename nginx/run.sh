#!/bin/sh
#
# configuration nginx
#
#
set -e

SED_REPLACE=`env | sed -e 's#\([^=]*\)=\(.*\)\s*$#s\#<\1>\#\2\#g;#'| tr '\n' ' ' | sed 's/$/\n/'`

[ -z "${APP}" -o -z "${ES_INDEX}" -o -z "${ES_HOST}" -o -z "${ES_PORT}" -o -z "${BACKEND_HOST}" -o -z "${BACKEND_PORT}" ] && echo "missing some env var" && exit 1

(
sed "${SED_REPLACE}" < /etc/nginx/nginx.template > /etc/nginx/nginx.conf
sed "${SED_REPLACE}" < /etc/nginx/conf.d/default.template > /etc/nginx/conf.d/default.conf
) && echo "nginx conf:" && cat /etc/nginx/nginx.conf && echo "default conf:" && cat /etc/nginx/conf.d/default.conf && nginx -g "daemon off;"
