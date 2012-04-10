from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes import generic

from models import Organization, Task, Project, Employee
from forms import EmployeeAdminForm
 

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm

    def save_model(self, request, employee, form, change):
        if not change:
            self.add_employee(request, employee, form, change)
        else:
            self.update_employee(request, employee, form, change)

    def add_employee(self,  request, employee, form, change):
        try:
            user_id = int(form.cleaned_data['user'])
            user = User.objects.get(id=user_id)
        except TypeError:
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            user = User(username=username, password=password, first_name=first_name,
                        last_name=last_name, email=email)
            user.save()

        employee.organization = form.cleaned_data['organization']
        employee.middle_name = form.cleaned_data['middle_name']       
        employee.user = user
        employee.save()

    def update_employee(self, request, employee, form, change):
        employee.user.username=form.cleaned_data['username']
        if 'password' in form.cleaned_data and form.cleaned_data['password']:
            employee.user.password=form.cleaned_data['password']
        print employee.user.password
        employee.user.first_name=form.cleaned_data['first_name']
        employee.user.last_name=form.cleaned_data['last_name']
        employee.user.email=form.cleaned_data['email']
        employee.middle_name = form.cleaned_data['middle_name']
        org_id = int(form.cleaned_data['organization'])
        org = Organization.objects.get(id=org_id)
        employee.organization = org
        user.save()
        employee.save()

# In a dreamless sleep he waits
admin.site.register(Employee, EmployeeAdmin) 
#admin.site.register(Employee) 
admin.site.register(Organization)
admin.site.register(Task)
admin.site.register(Project)

