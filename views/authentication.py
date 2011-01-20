from django.contrib import auth
from django.http import HttpResponseRedirect

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/netunong/login/")
