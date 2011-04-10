from django.contrib import admin
from register.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
 
class EmployeeProfileInline(admin.StackedInline):
    model = Employee
 
class EmployeeAdmin(UserAdmin):
    inlines = [EmployeeProfileInline]
 
admin.site.unregister(User)
admin.site.register(User, EmployeeAdmin) 

admin.autodiscover()
