
from django.conf.urls import url

from portal import views


urlpatterns = [
    url(r'^auth/$', views.auth),
]
