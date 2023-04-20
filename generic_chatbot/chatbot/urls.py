from django.urls import path, include
from datetime import datetime
from . import views

#url config 
urlpatterns = [
    path('chat', views.home, name='home')

]