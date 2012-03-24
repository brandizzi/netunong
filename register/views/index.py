from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.utils.translation import gettext as _

from register.models import Employee, Task, WorkingPeriod

@login_required 
def get_index(request):
    """
    Renderizes the initial page, where the user registers the beginning and
    end of working periods.
    """
    employee = request.user.get_profile()
    working_period = employee.last_working_period
    if working_period.is_closed():
        template = loader.get_template("register/open_period.html")
    else:
        template = loader.get_template("register/close_period.html")
    context = RequestContext(request, {
            'employee' : employee, 'working_period' : working_period
    })
    return HttpResponse(template.render(context))

@login_required
def open_period(request):
    """
    Opens a new working period.
    """
    employee = request.user.get_profile()
    intention = request.POST['intention']
    if not intention.strip():
        messages.error(request, _("What do you intend to do?"))
        return HttpResponseRedirect(reverse(get_index))
    task_id = request.POST['task']
    try:
        task_id = int(task_id)
        task = Task.objects.get(id=task_id) if task_id > 0 else None
    except ValueError:
        task = None
    start = datetime.now()
    working_period = WorkingPeriod(intended_task=task, employee=employee,
            intended=intention, start=start)
    working_period.save()
    return HttpResponseRedirect(reverse(get_index))

@login_required
def close_period(request):
    """
    Closes the last open working period of the user.
    """
    employee = request.user.get_profile()
    execution = request.POST['execution']
    working_period_id = int(request.POST['working_period'])
    working_period = WorkingPeriod.objects.get(id=working_period_id)
    if not execution.strip():
        messages.error(request, _("What did you do?"))
        return HttpResponseRedirect(reverse(get_index))
    working_period.executed = execution
    task_id = request.POST['task']
    try:
        task_id = int(task_id)
        task = Task.objects.get(id=task_id) if task_id > 0 else None
    except ValueError:
        task = None
    working_period.executed_task = task
    end = datetime.now()
    working_period.end = end
    working_period.save()
        
    return HttpResponseRedirect(reverse(get_index))


