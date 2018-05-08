#!/bin/sh

rm -rf blockchain/*
rm -rf key/*
echo > logs/sys.log
docker ps -a | awk '{print $1}' | xargs docker rm
