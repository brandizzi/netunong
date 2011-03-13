import views
from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template
urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^manage/$', views.manage),
    (r'^add/$', views.add),
)
