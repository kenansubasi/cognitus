#!/bin/sh

/code/docker/wait-for-it.sh db:5432 -- python manage.py migrate --noinput
/code/docker/wait-for-it.sh db:5432 -- python manage.py initdb
exec "$@"
