from django.conf.urls import patterns, url
from video import views


  
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r"^(?P<video_src>[\w.,/_\-\' ]+)$", views.index, name='index'),
)
