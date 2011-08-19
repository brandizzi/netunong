from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.utils.translation import gettext as _

from register.models import Employee, Task, WorkingPeriod
    
def get_index(request):
    employee = request.user.get_profile()
    working_period = employee.last_working_period
    if working_period.is_complete():
        template = loader.get_template("register/open_period.html")
    else:
        template = loader.get_template("register/close_period.html")
    context = RequestContext(request, {
            'employee' : employee, 'working_period' : working_period
    })
    return HttpResponse(template.render(context))

def post_to_index(request):
    employee = request.user.get_profile()
    operation = request.POST['operation']
    if operation == "open":
        intention = request.POST['intention']
        if not intention.strip():
            messages.error(request, _("What do you intend to do?"))
            return HttpResponseRedirect(reverse(index))
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
    elif operation == "close":
        execution = request.POST['execution']
        working_period_id = int(request.POST['working_period'])
        working_period = WorkingPeriod.objects.get(id=working_period_id)
        if not execution.strip():
            messages.error(request, _("What did you do?"))
            return HttpResponseRedirect(reverse(index))
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
        
    return HttpResponseRedirect(reverse(index))

functions = {
    'GET'  : get_index,
    'POST' : post_to_index
}

@login_required
def index(request):
    return functions[request.method](request)
    
