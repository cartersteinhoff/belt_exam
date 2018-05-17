from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^friends$', views.friends),
    url(r'^user/(?P<id>\d+)/$', views.user_profile),
    url(r'^friends/add/(?P<id>\d+)/$', views.add_friend),
    url(r'^friends/delete/(?P<id>\d+)/$', views.remove_friend),
]
