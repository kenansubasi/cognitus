#!/bin/sh

/code/docker/wait-for-it.sh web:8000
exec "$@"
