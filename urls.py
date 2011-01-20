from django.conf.urls.defaults import *
import django.contrib.auth.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^netunong/$', django.contrib.auth.views.login),
    (r'^netunong/register/', include('netunong.register.urls')),
    (r'^netunong/login/$', django.contrib.auth.views.login),
    (r'^netunong/logout/$', django.contrib.auth.views.logout, {'next_page': '/netunong/login/'}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
