import threading

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

from importer.agent import importer as importer_agent
from importer.agent import Exporter

def get_importer(request):
    if not importer_agent.is_running:
        template = loader.get_template("importer/index.html")
    else:
        template = loader.get_template("importer/running.html")
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def post_importer(request):
    url = request.POST['netuno-address']
    username = request.POST['username']
    password = request.POST['password']
    thread = threading.Thread(target=importer_agent.import_all, args=(url, username, password))
    thread.start()
    return HttpResponseRedirect('.')

importer_handlers = {
    'GET' : get_importer,
    'POST' : post_importer
}

def importer(request):
    return importer_handlers[request.method](request)


def get_exporter(request):
    if not importer_agent.is_running:
        template = loader.get_template("exporter/index.html")
    else:
        template = loader.get_template("importer/running.html")
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def post_exporter(request):
    url = request.POST['netuno-address']
    username = request.POST['username']
    password = request.POST['password']

    employee = request.user.get_profile()
    wps = employee.workingperiod_set.all()
    
    exporter = Exporter()
    exporter.export_logs(wps, url, username, password)
    return HttpResponseRedirect('.')

exporter_handlers = {
    'GET' : get_exporter,
    'POST' : post_exporter
}

def exporter(request):
    return exporter_handlers[request.method](request)
