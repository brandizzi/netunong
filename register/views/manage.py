from datetime import datetime, timedelta

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
    employee = request.user.get_profile()
    filter_params = {}
    startperiod = endperiod = ""
    selected_tasks = set()
    if 'startperiod' in request.GET and request.GET['startperiod']:
        startperiod = request.GET['startperiod']
        date = datetime.strptime(startperiod, NETUNONG_DATE_FORMAT)
        filter_params['start__gte'] = date
    if 'endperiod' in request.GET and request.GET['endperiod']:
        endperiod = request.GET['endperiod']
        date = datetime.strptime(endperiod, NETUNONG_DATE_FORMAT)
        date += timedelta(1)
        filter_params['end__lt'] = date
    if 'tasks' in request.GET and request.GET['tasks']:
        tasks_ids = request.GET.getlist('tasks')
        selected_tasks = set(Task.objects.get(id=task_id) for task_id in tasks_ids)
        filter_params['executed_task__in'] = selected_tasks
    wps = employee.workingperiod_set.filter(**filter_params)
    tasks = employee.tasks.all()
    template = loader.get_template("register/manage.html")
    context = RequestContext(request, {
            'employee' : employee, 'settings' : settings,
            'working_periods' : wps, 'startperiod' : startperiod,
            'endperiod' : endperiod, 'tasks' : tasks, 
            'selected_tasks' : selected_tasks,
    })
    return HttpResponse(template.render(context))

def post_manage(request):

    if request.POST.has_key('update'):
        working_period_id = request.POST['update']
        working_period = WorkingPeriod.objects.get(id=int(working_period_id))
        activity = request.POST['activity'+working_period_id]
        task_id = request.POST['task'+working_period_id]
        try:
            task_id = int(task_id)
            task = Task.objects.get(id=task_id) if task_id > 0 else None
        except ValueError:
            task = working_period.last_task
        start_date = request.POST['start-date'+working_period_id]
        end_date = request.POST['end-date'+working_period_id]
        start_time = request.POST['start-time'+working_period_id]
        end_time = request.POST['end-time'+working_period_id]
        
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
    elif  request.POST.has_key('delete'):
        working_period_id = request.POST['delete']
        working_period = WorkingPeriod.objects.get(id=int(working_period_id))
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
