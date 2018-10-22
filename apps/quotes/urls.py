from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^create$', views.create),
    url(r'^like$', views.like),
    url(r'^user/(?P<num>\d+)$', views.user),
    url(r'^delete$', views.delete),
    url(r'^edituser$', views.editUser),
    url(r'^edit_submit$', views.updateUser)
]