from django.conf.urls.defaults import *
import django.contrib.auth.views
import netunong.view
import netunong.views.authentication
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^netunong/$', netunong.view.current_datetime),
    (r'^netunong/login/$', django.contrib.auth.views.login),
    (r'^netunong/logout/$', netunong.views.authentication.logout)

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
