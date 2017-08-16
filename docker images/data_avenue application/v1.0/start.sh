#!/bin/sh
set -e
IP=$1
echo $IP dataavenue.database >> /etc/hosts
catalina.sh run

