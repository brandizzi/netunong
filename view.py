from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render_to_response

import datetime
def current_datetime(request):
    template = loader.get_template("index.html")
    context = RequestContext(request)
    return HttpResponse(template.render(context))

