from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_stream, name='home')
]