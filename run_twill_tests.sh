#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=settings 
export PYTHONPATH=. 
. ~/Library/flunc/bin/activate
python cleartest.py
echo 'RUNNING TESTS FOR APPLICATION register'
flunc -ptwill all
