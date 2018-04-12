from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/ping/(?P<id>[0-9]+)/$', consumers.DamesPing)
]