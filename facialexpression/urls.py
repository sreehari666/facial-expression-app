from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('ajax/getData',views.getData,name='getData'),
    
]