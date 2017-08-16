#!/bin/sh
set -e
VARIABLE=$1
# first arg is `-f` or `--some-option`
if [ "${1#-}" != "$1" ]; then
	set -- haproxy "$@"
fi

if [ "$1" = 'haproxy' ]; then
	# if the user wants "haproxy", let's use "haproxy-systemd-wrapper" instead so we can have proper reloadability implemented by upstream
	shift # "haproxy"
	set -- "$(which haproxy-systemd-wrapper)" -p /run/haproxy.pid "$@"
fi

useradd haproxy
chmod +x /etc/init.d/haproxy

# Start consul-template service
consul-template -consul ${VARIABLE}:8500 -template "/etc/haproxy/template.ctmpl:/etc/haproxy/thaproxy.cfg:service haproxy restart"
exec "$@"
