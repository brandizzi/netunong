from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes import generic

from models import Organization, Task, Project, Employee
from forms import EmployeeAdminForm
 

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm

    def save_model(self, request, employee, form, change):
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        first_name=form.cleaned_data['first_name']
        last_name=form.cleaned_data['last_name']
        email=form.cleaned_data['email']
        user = User(username=username, password=password, first_name=first_name,
                    last_name=last_name, email=email)
        user.save()
        employee.user = user
        employee.save()
# In a dreamless sleep he waits
admin.site.register(Employee, EmployeeAdmin) 
#admin.site.register(Employee) 
admin.site.register(Organization)
admin.site.register(Task)
admin.site.register(Project)

