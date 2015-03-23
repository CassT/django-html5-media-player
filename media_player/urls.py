from django.conf.urls import patterns, url
from media_player import views


urlpatterns = patterns('',
#    url(r"^(?P<media_src>[\w.,/_\-\'\!\[\]\&\% ]+)$", views.media_player, name='media_player'),
    url(r'^(?P<media_src>.*)$',views.media_player, name='media_player'),
)
