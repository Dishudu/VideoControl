from django.urls import path
from .consumers import VideoStreamConsumer, BrowserVideoConsumer

websocket_urlpatterns = [
    path('ws/video/', VideoStreamConsumer.as_asgi()),
    path('ws/browser/', BrowserVideoConsumer.as_asgi()),
]