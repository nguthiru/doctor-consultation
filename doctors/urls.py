from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('',DoctorViewSet)
router.register('consultation',ConsultationViewset,basename='consult_doctor')
urlpatterns = [
    path('register/',register_doctor,name='register_doctor'),
    path('schedule/',consultation_schedule,name='consultation_schedule')
]+router.urls