from django.urls import path,include
from .views import *
urlpatterns = [
    path('register/',register_patient,name='register_patient')
]