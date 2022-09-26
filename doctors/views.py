from urllib import request
from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from patients.models import Ticket
from patients.serializers import TicketSerializer
from .models import Consultation, Doctor
from rest_framework.decorators import api_view
from .serializers import ConsultationSerializer, DoctorSerializer
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

class DoctorViewSet(viewsets.ModelViewSet):

    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

@api_view(['GET'])
def consultation_schedule(request):
    doctor = get_object_or_404(Doctor,user=request.user)

    tickets = Ticket.objects.filter(application__doctor=doctor,completed=False)

    tickets_serial = TicketSerializer(tickets,many=True)

    return Response(tickets_serial.data)

class ConsultationViewset(viewsets.ModelViewSet):
    serializer_class = ConsultationSerializer
    
    def get_queryset(self):
        doc = get_object_or_404(Doctor,user=request.user)
        return Consultation.objects.filter(ticket__application_doctor=doc)