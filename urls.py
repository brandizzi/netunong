from django.conf.urls.defaults import *
import django.contrib.auth.views
import django.contrib.admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^netunong/$', django.contrib.auth.views.login),
    (r'^netunong/register/', include('netunong.register.urls')),
    (r'^netunong/login/(?:\?next=.*)?$', django.contrib.auth.views.login), # (?:...) requird for non grouping
    (r'^accounts/login/(?:\?next=.*)?$', django.contrib.auth.views.login),
    (r'^netunong/logout/$', django.contrib.auth.views.logout, {'next_page': '/netunong/login/'}),
    (r'^admin/', include(django.contrib.admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
