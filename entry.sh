#!/bin/sh

mkdir -p /data/audio
mkdir -p /data/ebook
# start cron
/usr/sbin/crond -f -l 8
