import views.index
import views.manage
import views.add
from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template
urlpatterns = patterns('',
    (r'^$', views.index.get_index),
    (r'^open/$', views.index.open_period),
    (r'^close/$', views.index.close_period),
    (r'^manage/$', views.manage.manage),
    (r'^add/$', views.add.add),
)
