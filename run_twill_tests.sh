#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=settings 
export PYTHONPATH=. 
python cleartest.py
echo 'STARTING NETUNONG'
python manage.py runserver 32198 > netunong.log &
python importer/tests/netunomock/server.py &
MPID=$!
sleep 1
echo 'RUNNING TESTS FOR APPLICATIONS: register, importer'
if [ "$1" ] ; then
flunc -ptwill $1
else
flunc -ptwill all
fi
kill $(ps -opid,command | awk '/runserver 32198/{if(!/awk/)print $1}')
kill $MPID
