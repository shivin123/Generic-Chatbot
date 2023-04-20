from django.contrib import admin
from django.urls import path,include
import chatbot.views as views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('chatbot.urls')),
    path('', views.home, name='home')
]
