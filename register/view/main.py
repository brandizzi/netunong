from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import gettext as _

from register.models import Employee, Task, WorkingPeriod
    
def get_index(request):
    employee = Employee.objects.get(user=request.user)
    working_period = employee.last_working_period
    if working_period.is_complete():
        template = loader.get_template("open_period.html")
    else:
        template = loader.get_template("close_period.html")
    context = RequestContext(request, {
            'employee' : employee, 'working_period' : working_period
    })
    return HttpResponse(template.render(context))

def post_to_index(request):
    errors = []
    employee = Employee.objects.get(user=request.user)
    operation = request.POST['operation']
    if operation == "open":
        intention = request.POST['intention']
        if not intention.strip():
            errors.append(_("What is your intention?"))
            template = loader.get_template("open_period.html")
            context = RequestContext(request, {
                    'employee' : employee, 'errors' : errors
            })
            return HttpResponse(template.render(context))
        task_id = request.POST['task']
        if task_id.strip():
            task = Task.objects.get(id=task_id)
        else:
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
            errors.append(_("What did you do?"))
            template = loader.get_template("close_period.html")
            context = RequestContext(request, {
                    'employee' : employee, 
                    'working_period' : working_period, 
                    'errors' : errors
            })
            return HttpResponse(template.render(context))
        working_period.executed = execution
        task_id = request.POST['task']
        if task_id.strip():
            task = Task.objects.get(id=task_id)
        else:
            task = None
        working_period.executed_task = task
        end = datetime.now()
        working_period.end = end
        working_period.save()
        
    return HttpResponseRedirect('.')

functions = {
    'GET'  : get_index,
    'POST' : post_to_index
}

def index(request):
    return functions[request.method](request)
    
