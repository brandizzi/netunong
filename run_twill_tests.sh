#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=settings 
python cleartest.py
echo 'RUNNING TESTS FOR APPLICATION register'
twill-sh $TWILL_TEST_PARAMS twill/register/*.tw
