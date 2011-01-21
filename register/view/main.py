from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import render_to_response

from register.models import Employee, Task, WorkingPeriod
    
def get_index(request):
    employee = Employee.objects.get(user=request.user)
    working_period = employee.get_last_working_period()
    if working_period.is_complete():
        template = loader.get_template("open_period.html")
    else:
        template = loader.get_template("close_period.html")
    context = RequestContext(request, {
            'employee' : employee, 'working_period' : working_period
    })
    return HttpResponse(template.render(context))

def post_to_index(request):
    employee = Employee.objects.get(user=request.user)
    operation = request.POST['operation']
    if operation == "open":  
        task_id = int(request.POST['task'])
        task = Task.objects.get(id=task_id)
        intention = request.POST['intention']
        start = datetime.now()

        working_period = WorkingPeriod(intended_task=task, employee=employee,
                intended=intention, start=start)
        working_period.save()
    elif operation == "close":
        task_id = int(request.POST['task'])
        task = Task.objects.get(id=task_id)
        executed = request.POST['execution']
        end = datetime.now()

        working_period_id = int(request.POST['working_period'])
        working_period = WorkingPeriod.objects.get(id=working_period_id)
        working_period.executed = executed
        working_period.executed_task = task
        working_period.end = end
        working_period.save()
        
    return HttpResponseRedirect('.')

functions = {
    'GET'  : get_index,
    'POST' : post_to_index
}

def index(request):
    return functions[request.method](request)
    
