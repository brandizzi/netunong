#!/usr/bin/env DJANGO_SETTINGS_MODULE=settings python
from register.models import Employee
from register.test.test_utilities import get_organization_project_task, get_employee

organization, project, task = get_organization_project_task()
test_user = get_employee(organization)
print "User test created"
