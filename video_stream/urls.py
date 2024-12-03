from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_stream, name='home'),
    path('relay-control/', views.relay_control, name='relay_control'),
]