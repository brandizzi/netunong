from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import gettext as _
from django.conf import settings

from register.models import Employee, Task, WorkingPeriod

def manage(request):
    employee = Employee.objects.get(user=request.user)
    template = loader.get_template("register/manage.html")
    context = RequestContext(request, {
            'employee' : employee, 'settings' : settings
    })
    return HttpResponse(template.render(context))
