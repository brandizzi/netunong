from django.conf.urls.defaults import patterns

import importer.views

urlpatterns = patterns('',
    (r'^$', importer.views.index),
)
