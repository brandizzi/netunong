from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.utils.translation import gettext as _

from register.models import Employee, Task, WorkingPeriod
from settings import NETUNONG_DATE_FORMAT, NETUNONG_TIME_FORMAT

def get_add(request):
    employee = request.user.get_profile()
    template = loader.get_template("register/add.html")
    context = RequestContext(request, {'employee' : employee})
    return HttpResponse(template.render(context))

def post_to_add(request):
    employee = request.user.get_profile()
    activity = request.POST['activity']
    task_id = request.POST['task']
    if not activity.strip():
        messages.error(request, _("What did you do?"))
        return HttpResponseRedirect(reverse(add))
    try:
        task_id = int(task_id)
        task = Task.objects.get(id=task_id) if task_id > 0 else None
    except ValueError:
        messages.error(request, _("What task did you help?"))
        return HttpResponseRedirect(reverse(add))

    start_date = request.POST['start-date']
    end_date = request.POST['end-date']
    start_time = request.POST['start-time']
    end_time = request.POST['end-time']

    if not start_date.strip() or not start_time.strip():
        messages.error(request, _("When did you start this period?"))
        return HttpResponseRedirect(reverse(add))
    
    if not end_date.strip() or not end_time.strip():
        messages.error(request, _("When did you end this period?"))
        return HttpResponseRedirect(reverse(add))

    try:
        start = datetime.strptime(start_date+" "+start_time,
                NETUNONG_DATE_FORMAT+" "+NETUNONG_TIME_FORMAT)
    except ValueError:
        messages.error(request, _("Your start date or time is invalid."))
        return HttpResponseRedirect(reverse(add))
    
    try:
        end = datetime.strptime(end_date+" "+end_time,
                NETUNONG_DATE_FORMAT+" "+NETUNONG_TIME_FORMAT)
    except ValueError:
        messages.error(request, _("Your end date or time is invalid."))
        return HttpResponseRedirect(reverse(add))
    working_period = WorkingPeriod(executed_task=task, employee=employee,
                executed=activity, start=start, end=end)
    working_period.save()
    messages.success(request, _("Period registered."))
    # TODO use reverse
    return HttpResponseRedirect('/netunong/manage')

functions = {
    'GET'  : get_add,
    'POST' : post_to_add
}

@login_required
def add(request):
    return functions[request.method](request)
    
