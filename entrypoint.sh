#!/bin/sh
set -e
service ssh start
exec gunicorn -w 4 -b 0.0.0.0:3100 main:app