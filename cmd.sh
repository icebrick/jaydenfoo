#!/usr/bin/env bash

#STATIC_DIR=./static_collect
#
#if [ -d "$STATIC_DIR" ]; then
#    rm -r "$STATIC_DIR"
#fi
#
#python3 manage.py collectstatic
cd deploy
docker-compose up --build -d