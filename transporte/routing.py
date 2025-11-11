from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Motorista/cliente se conecta aqui: ws://host/ws/locations/
    re_path(r'ws/locations/$', consumers.LocationConsumer.as_asgi()),
    # Para grupos por linha (opcional): ws://host/ws/locations/LC01/
    re_path(r'ws/locations/(?P<linha_codigo>[A-Za-z0-9_-]+)/$', consumers.LocationConsumer.as_asgi()),
]
