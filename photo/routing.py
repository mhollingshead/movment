from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path('<int:video_id>/watch', consumers.WatchConsumer, name='watch'),
]
