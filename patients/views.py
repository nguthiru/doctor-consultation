import imp
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Patient
from rest_framework.decorators import api_view
from .serializers import PatientSerializer
# Create your views here.
@api_view(['POST'])
def register_patient(request):
    patient = Patient(user=request.user)

    patient_serial = PatientSerializer(instance=patient,data=request.data)

    if patient_serial.is_valid():
        patient_serial.save()
        return Response(status=201)
    else:
        return Response(status=400,data=patient_serial.errors)



