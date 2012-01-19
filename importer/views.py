import threading

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

from importer.agent import importer

def get_index(request):
    if not importer.is_running:
        template = loader.get_template("importer/index.html")
    else:
        template = loader.get_template("importer/running.html")
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def post_index(request):
    url = request.POST['netuno-address']
    username = request.POST['username']
    password = request.POST['password']
    thread = threading.Thread(target=importer.import_all, args=(url, username, password))
    thread.start()
    return HttpResponseRedirect('.')

handlers = {
    'GET' : get_index,
    'POST' : post_index
}

def index(request):
    return handlers[request.method](request)

