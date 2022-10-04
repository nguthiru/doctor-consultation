from rest_framework.serializers import ModelSerializer
from .models import *
class SpecializationSerializer(ModelSerializer):

    class Meta:
        fields='__all__'
        model= Specialization
class DoctorSerializer(ModelSerializer):
    specialization = SpecializationSerializer()
    class Meta:
        fields = '__all__'
        model = Doctor
        extra_kwargs = {'user': {'required': False}}



class ConsultationSerializer(ModelSerializer):
    from patients.serializers import TicketSerializer
    ticket = TicketSerializer()
    class Meta:
        fields = '__all__'
        model = Consultation