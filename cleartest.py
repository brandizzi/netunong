#!/usr/bin/env DJANGO_SETTINGS_MODULE=settings python
import django.contrib.auth.models as am

try:
    test_user = am.User.objects.get(username='test')
    print "User test found"
    test_user.delete()
    print "User test deleted"
except am.DoesNotExist:
    print "User test not found"
