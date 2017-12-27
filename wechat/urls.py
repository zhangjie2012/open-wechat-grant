
from django.conf.urls import url

from wechat.views import callback
from wechat.views import timed

urlpatterns = [
    # 微信服务器回调接口
    url(r'^auth_callback/$', callback.auth),
    url(r'^grant_callback/$', callback.grant, name='grant'),

    # 需要定时执行的接口
    url(r'^update_component_token/$', timed.update_component_token),
    url(r'^update_auth_access_token/$', timed.update_auth_access_token),
]
