#!/usr/bin/env DJANGO_SETTINGS_MODULE=settings python
from register.models import Employee
from register.test.test_utilities import get_organization, get_employee

test_user = get_employee()
print "User test created"
