#!/usr/bin/env DJANGO_SETTINGS_MODULE=settings python
import django.contrib.auth.models as am


test_user = am.User.objects.create_user(
        username='test', 
        password='test', 
        email='test')
print "User test created"
