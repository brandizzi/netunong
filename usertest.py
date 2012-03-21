#!/usr/bin/env DJANGO_SETTINGS_MODULE=settings python
from register.models import Employee, Task
from register.tests.test_utilities import get_organization_project_task, get_employee

organization, project, task = get_organization_project_task()
task2 = Task(project=project, name='some task', description='SOME TASK')
task2.save()
test_user = get_employee(organization=organization, task=task)
test_user.tasks.add(task2)
test_user.save()
print "User test created"
