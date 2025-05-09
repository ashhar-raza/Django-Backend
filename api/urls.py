from home.views import *
from django.urls import path

urlpatterns = [
    path('index', index),
    path('user',user_api),
    path('user/login',login_api),
    path('notes', notes_api),
    path('person',person), 
    ]
    
