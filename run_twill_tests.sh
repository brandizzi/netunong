#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE=settings 
python cleartest.py
twill-sh $TWILL_TEST_PARAMS twill/*.tw
