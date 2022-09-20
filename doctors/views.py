from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Doctor
from rest_framework.decorators import api_view
from .serializers import DoctorSerializer
# Create your views here.
@api_view(['POST'])
def register_doctor(request):
    doctor = Doctor(user=request.user)

    doctor_serial = DoctorSerializer(instance=doctor,data=request.data)

    if doctor_serial.is_valid():
        doctor_serial.save()
        return Response(status=201)
    else:
        return Response(status=400,data=doctor_serial.errors)
