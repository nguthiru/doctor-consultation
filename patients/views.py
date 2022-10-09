import imp
from urllib import request
from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from doctors.models import Consultation, Doctor
from doctors.serializers import ConsultationSerializer
from .models import Application, Patient, Ticket, TicketMedia
from rest_framework.decorators import api_view,action
from .serializers import ApplicationSerializer, PatientSerializer, TicketMediaSerializer
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
@api_view(['GET'])
def apply_consultation(request,doctor):
    doctor = get_object_or_404(Doctor,id=doctor)
    patient = get_object_or_404(Patient,user=request.user)
    application = Application(patient-patient,doctor=doctor)
    application_serial = ApplicationSerializer(application)
    if application_serial.is_valid():
        application_serial.save()
        return Response(application_serial.data,status=201)
    else:
        return Response(application_serial.errors)

@api_view(['POST'])
def make_payment(request,id):
    application = get_object_or_404(Application,id=id)
    if application.patient.user == request.user:
        pass
    # initiate mpesa payment

class ConsultationViewset(viewsets.ModelViewSet):
    serializer_class = ConsultationSerializer

    def get_queryset(self):
        patient = get_object_or_404(Patient,user=self.request.user)
        return Consultation.objects.filter(ticket__application__patient=patient,ticket__completed=False)
    
    @action(methods=['GET'],detail=False)
    def completed(self,request,*args,**kwargs):
        patient = get_object_or_404(Patient,user=self.request.user)

        qs = Consultation.objects.filter(ticket__application__patient=patient,ticket__completed=True)

        return Response(ConsultationSerializer(qs,many=True).data)
@api_view(['GET'])
def get_media(request,id):
    ticket = get_object_or_404(Ticket,id=id)
    media = TicketMedia.objects.filter(ticket=ticket)
    return Response(TicketMediaSerializer(media,many=True).data)

class TicketMediaViewSet(viewsets.ModelViewSet):
    serializer_class = TicketMediaSerializer

    def get_queryset(self):
        return TicketMedia.objects.filter(sender=self.request.user)