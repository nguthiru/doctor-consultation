from operator import imod
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth import get_user
from rest_framework.response import Response
from accounts.serializers import UserSerializer
# Create your views here.
@api_view(['GET'])
def me(request):
    serial = UserSerializer(request.user)

    return Response(serial.data)


