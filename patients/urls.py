from unicodedata import name
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register('consultation',ConsultationViewset,basename='consult')
router.register('media',TicketMediaViewSet,basename='media')
urlpatterns = [
    path('register/',register_patient,name='register_patient'),
    path('consultation/media/<int:id>/',get_media)
]+router.urls