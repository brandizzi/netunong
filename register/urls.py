import views
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', views.index),
)
