from email.mime import application
from rest_framework.serializers import ModelSerializer
from .models import *
from doctors.serializers import DoctorSerializer
class PatientSerializer(ModelSerializer):

    class Meta:
        model = Patient
        fields = "__all__"
        extra_kwargs = {'user': {'required': False}}

class ApplicationSerializer(ModelSerializer):
    doctor = DoctorSerializer()
    patient = PatientSerializer()
    class Meta:
        model = Application
        fields = '__all__'
        extra_kwargs = {'patient':{'required':False}}

class TicketSerializer(ModelSerializer):
    application = ApplicationSerializer()

    class Meta:
        model = Ticket
        fields = '__all__'