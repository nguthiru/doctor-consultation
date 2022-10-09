from django.urls import path,include
from .views import *
urlpatterns = [
  
    path('', include('rest_auth.urls')),
    path('register/', include('rest_auth.registration.urls')),
    path('me/',me),
]