from django.urls import path,include

from .views import *
urlpatterns = [
  
    path('', include('rest_auth.urls')),
    path('register/', register),
    path('me/',me),
    path('update/profile/',update_profile),
    
]