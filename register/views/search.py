from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from register.models import Task
import register.views.manage

@login_required
def search_tasks(request):
    if 'operation' in request.GET and request.GET['operation'] == 'select':
        url = "%s?%s" % (reverse(register.views.manage.manage), request.META['QUERY_STRING'])
        print>>file('f','a'), url
        return HttpResponseRedirect(url)
    startperiod = endperiod = ""
    task_ids = []
    if 'startperiod' in request.GET and request.GET['startperiod']:
        startperiod = request.GET['startperiod']
    if 'endperiod' in request.GET and request.GET['endperiod']:
        endperiod = request.GET['endperiod']
    if 'tasks' in request.GET and request.GET['tasks']:
        task_ids = request.GET.getlist('tasks')
    # TODO to conditioning to permission
    tasks = Task.objects.all()
    template = loader.get_template("register/list_tasks.html")
    context = RequestContext(request, {
            'startperiod' : startperiod, 'endperiod' : endperiod, 
            'tasks' : tasks,
    })
    return HttpResponse(template.render(context))

