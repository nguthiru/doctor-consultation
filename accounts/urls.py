from django.urls import path,include

urlpatterns = [
  
    path(r'^rest-auth/', include('rest_auth.urls'))
]