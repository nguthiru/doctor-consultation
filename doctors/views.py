from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from patients.models import Patient, Ticket, User
from .models import Consultation, Doctor, Specialization
from rest_framework.decorators import api_view,action,permission_classes
from rest_framework.permissions import IsAdminUser
from .serializers import ConsultationSerializer, DoctorSerializer, DoctorWriteSerializer, SpecializationSerializer
from django.contrib.auth import get_user
from django.db.models import DateField, Sum,Count
# Create your views here.
@api_view(['POST'])
def register_doctor(request):
    doctor = Doctor(user=request.user)
    doctor_serial = DoctorWriteSerializer(instance=doctor,data=request.data)
    try:
        doc= Doctor.objects.get(user=request.user)
        return Response({'non_field_errors':'doctor already exists'},status=400)
    except Doctor.DoesNotExist:
        if doctor_serial.is_valid():
            user = request.user
            user.is_doctor = True
            
            user.save()
            doctor_serial.save()
            
            return Response(status=201)
        else:
            return Response(status=400,data=doctor_serial.errors)
@api_view(['GET'])
def specialities(request):
    qs = Specialization.objects.all()
    serial = SpecializationSerializer(qs,many=True)
    return Response(serial.data)
class DoctorViewSet(viewsets.ModelViewSet):

    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

@api_view(['GET'])
def consultation_schedule(request):
    from patients.serializers import TicketSerializer

    doctor = get_object_or_404(Doctor,user=request.user)

    tickets = Ticket.objects.filter(application__doctor=doctor,completed=False)

    tickets_serial = TicketSerializer(tickets,many=True)

    return Response(tickets_serial.data)


class ConsultationViewset(viewsets.ModelViewSet):
    serializer_class = ConsultationSerializer
    
    def get_queryset(self):
        doc = get_object_or_404(Doctor,user=self.request.user)
        return Consultation.objects.filter(ticket__application__doctor=doc,ticket__completed=True)


    @action(['GET'],detail=True)
    def start(self,request,pk):
        ticket = get_object_or_404(Ticket,id=pk)
        ticket.completed = True
        ticket.save()
        Consultation.objects.create(ticket=ticket)
        return Response(status=200)

@api_view(['GET'])
def consultation_details(request,id):
    consult = get_object_or_404(Consultation,ticket=id)

    return Response(ConsultationSerializer(consult,context={"request": request}).data)

@permission_classes([IsAdminUser])
@api_view(['GET'])
def report(request):
    number_of_doctors = Doctor.objects.all().count()
    patients_under_consultation = Consultation.objects.filter(ticket__completed=True,diagnosis=None).count()

    patients_number = Patient.objects.all().count()
    diagnosis = Consultation.objects.all().values('diagnosis').annotate(count=Count('id'))
    special_doctors = Doctor.objects.all().values('specialization','specialization__name').annotate(count=Count('id'))

    return Response(data={
        'doctors':number_of_doctors,
        "patients":patients_number,
        "patients_consult":patients_under_consultation,
        "diagnosis":diagnosis,
        "specializations":special_doctors
    })