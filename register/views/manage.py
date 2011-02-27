from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.utils.translation import gettext as _

from register.models import Employee, Task, WorkingPeriod

from settings import NETUNONG_DATE_FORMAT, NETUNONG_TIME_FORMAT

def get_manage(request):
    employee = Employee.objects.get(user=request.user)
    template = loader.get_template("register/manage.html")
    context = RequestContext(request, {
            'employee' : employee, 'settings' : settings
    })
    return HttpResponse(template.render(context))

def post_manage(request):
    working_period_id = request.POST['working_period']
    working_period = WorkingPeriod.objects.get(id=int(working_period_id))

    if request.POST.has_key('submit%s' % working_period_id):
        activity = request.POST['activity']
        task_id = request.POST['task']
        try:
            task_id = int(task_id)
            task = Task.objects.get(id=task_id) if task_id > 0 else None
        except ValueError:
            task = working_period.last_task
        start_date = request.POST['start-date']
        end_date = request.POST['end-date']
        start_time = request.POST['start-time']
        end_time = request.POST['end-time']
        
        try:
            start = datetime.strptime(start_date+" "+start_time,
                    NETUNONG_DATE_FORMAT+" "+NETUNONG_TIME_FORMAT)
        except ValueError:
            start = working_period.start
        
        try:
            end = datetime.strptime(end_date+" "+end_time,
                    NETUNONG_DATE_FORMAT+" "+NETUNONG_TIME_FORMAT)
        except ValueError:
            end = working_period.end
        
        working_period.executed = activity
        working_period.executed_task = task
        working_period.start = start
        working_period.end = end
        working_period.save()
        # TODO identify the working period
        messages.success(request, _("The working period was udpated!"))
    elif  request.POST.has_key('delete%s' % working_period_id):
        working_period.delete()
        # TODO identify the working period
        messages.success(request, _("The working period was deleted!"))
    return HttpResponseRedirect(reverse(manage))

functions = {
    'GET'  : get_manage,
    'POST' : post_manage
}

@login_required
def manage(request):
    return functions[request.method](request)
