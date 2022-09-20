from django.urls import path,include
from .views import *
urlpatterns = [
    path('register/',register_doctor,name='register_doctor')
]