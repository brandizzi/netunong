#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=settings 
export PYTHONPATH=. 
python cleartest.py
echo 'STARTING NETUNONG'
python manage.py runserver 32198 > netunong.log &
sleep 1
echo 'RUNNING TESTS FOR APPLICATION register'
flunc -ptwill all
kill $(ps -opid,command | awk '/runserver 32198/{if(!/awk/)print $1}')
