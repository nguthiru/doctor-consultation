import imp
import json
from urllib import request
from django.shortcuts import render, get_object_or_404
import requests
from rest_framework import viewsets
from rest_framework.response import Response

from doctors.models import Consultation, Doctor
from doctors.serializers import ConsultationSerializer
from patients.mpesa import LipaNaMpesaPass, MpesaAccessToken
from .models import Application, Patient, Ticket, TicketMedia
from rest_framework.decorators import api_view, action
from .serializers import ApplicationSerializer, PatientSerializer, TicketMediaSerializer
# Create your views here.


@api_view(['POST'])
def register_patient(request):
    patient = Patient(user=request.user)
    print(request.data)
    patient_serial = PatientSerializer(instance=patient, data=request.data)

    if patient_serial.is_valid():
        patient_serial.save()
        return Response(status=201)
    else:
        return Response(status=400, data=patient_serial.errors)


@api_view(['GET'])
def apply_consultation(request, doctor):
    doctor = get_object_or_404(Doctor, id=doctor)
    patient = get_object_or_404(Patient, user=request.user)
    application = Application(patient-patient, doctor=doctor)
    application_serial = ApplicationSerializer(application)
    if application_serial.is_valid():
        application_serial.save()
        return Response(application_serial.data, status=201)
    else:
        return Response(application_serial.errors)


@api_view(['POST'])
def make_payment(request, id):
    application = get_object_or_404(Application, id=id)
    if application.patient.user == request.user:
        pass
    # initiate mpesa payment


class ConsultationViewset(viewsets.ModelViewSet):
    serializer_class = ConsultationSerializer

    def get_queryset(self):
        patient = get_object_or_404(Patient, user=self.request.user)
        return Consultation.objects.filter(ticket__application__patient=patient, ticket__completed=True)

    @action(methods=['GET'], detail=False)
    def completed(self, request, *args, **kwargs):
        patient = get_object_or_404(Patient, user=self.request.user)

        qs = Consultation.objects.filter(
            ticket__application__patient=patient, ticket__completed=False)

        return Response(ConsultationSerializer(qs, many=True).data)


@api_view(['GET'])
def get_media(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    media = TicketMedia.objects.filter(ticket=ticket)
    return Response(TicketMediaSerializer(media, many=True, context={'request': request}).data)


@api_view(['POST'])
def make_payment(request):
    
    data = request.data
    phone = str(data['phone'])
    if phone.startswith('0'):
        phone = phone.replace('0','254',1)
    doctor = get_object_or_404(Doctor, id=data['doctor'])
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {MpesaAccessToken().access_token}'
    }
    payload = {
        "BusinessShortCode": LipaNaMpesaPass.Business_short_code,
        "Password": LipaNaMpesaPass.decode_password,
        "Timestamp": LipaNaMpesaPass.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 5,
        "PartyA": phone,
        "PartyB": 174379,
        "PhoneNumber": phone,
        "CallBackURL": "https://google.com",
        "AccountReference": f"{doctor.id} appoint",
        "TransactionDesc": "SaveSpace",
    }
    response = requests.post(
        'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers=headers, json=payload)

    if response.status_code <= 210:
        print(request.user)
        patient = get_object_or_404(Patient, user=request.user)
        data_payment = json.loads(response.text)
        merchantID = data_payment['MerchantRequestID']
        checkoutID = data_payment['CheckoutRequestID']
        application = Application.objects.create(
            patient=patient, doctor=doctor, merchantID=merchantID, checkoutID=checkoutID)

    return Response(ApplicationSerializer(application).data, status=response.status_code)
    
class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(patient__user=self.request.user)



@api_view(['POST'])
def verify_payment(request):
    data = request.data
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {MpesaAccessToken().access_token}'
    }
    payload = {
        "BusinessShortCode": LipaNaMpesaPass.Business_short_code,
        "Password": LipaNaMpesaPass.decode_password,
        "Timestamp": LipaNaMpesaPass.lipa_time,
        "CheckoutRequestID": data["checkoutID"],
    }
    checkoutID = data['checkoutID']
    response = requests.post(api_url, headers=headers, json=payload)
    response_data = json.loads(response.text)
    if (response.status_code <= 210):
        application = Application.objects.get(checkoutID=checkoutID)
        response_code = response_data['ResultCode']
        if int(response_code) == 0:
            Ticket.objects.create(application=Application)
            return Response(status=201)
    return Response(data=response_data, status=400)


class TicketMediaViewSet(viewsets.ModelViewSet):
    serializer_class = TicketMediaSerializer

    def get_serializer_context(self):
        context = super(TicketMediaViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return TicketMedia.objects.filter(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        ticket = TicketMedia(sender=request.user)
        serializer = TicketMediaSerializer(instance=ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
