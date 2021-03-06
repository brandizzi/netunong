from django.conf.urls.defaults import *
from django.conf import settings
import django.contrib.auth.views
import django.contrib.admin
import django.views.static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
STATIC_ROOT=    'static'
django.contrib.admin.autodiscover()
patterns_list = [
    # Example:
    (r'^netunong/login/$', django.contrib.auth.views.login),
    (r'^netunong/', include('register.urls')),
    (r'^netunong/login/(?:\?next=.*)?$', django.contrib.auth.views.login), # (?:...) requird for non grouping
    (r'^accounts/login/(?:\?next=.*)?$', django.contrib.auth.views.login),
    (r'^netunong/logout/$', django.contrib.auth.views.logout, {'next_page': '/netunong/login/'}),

    (r'^admin/', include(django.contrib.admin.site.urls)),

    (r'^netunong/heritage/', include('importer.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # (r'^netunong/reports/', include('netunong.reports.urls')),
]

if settings.DEBUG:
    patterns_list.append(
        (r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root':settings.STATIC_ROOT}),
    )

urlpatterns = patterns('', *patterns_list)
