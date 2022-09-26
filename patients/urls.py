from unicodedata import name
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register('consultation',ConsultationViewset,basename='consult')
urlpatterns = [
    path('register/',register_patient,name='register_patient')
]+router.urls