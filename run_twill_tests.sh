#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=twill_settings 
export PYTHONPATH=. 

django-admin.py syncdb
django-admin.py migrate register
django-admin.py migrate importer

python cleartest.py

echo 'STARTING NETUNONG'
django-admin.py runserver 32198 > netunong.log &

python importer/tests/netunomock/server.py &
MPID=$!
sleep 1
echo 'RUNNING TESTS FOR APPLICATIONS: register, importer'
if [ "$1" ] ; then
flunc -ptwill $1
else
flunc -ptwill all
fi
RESULT=$?
kill $(ps -opid,command | awk '/runserver 32198/{if(!/awk/)print $1}')
kill $MPID
exit $RESULT
