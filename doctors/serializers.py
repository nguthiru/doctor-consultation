from asyncore import read
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import *

class SpecializationSerializer(ModelSerializer):

    class Meta:
        fields='__all__'
        model= Specialization
class DoctorSerializer(ModelSerializer):
    specialization = SpecializationSerializer()
    # image = SerializerMethodField('get_image')
    class Meta:
        fields = '__all__'
        model = Doctor
        extra_kwargs = {'user': {'required': False},'specialization':{'required':False}}
    
    def create(self, validated_data):
        specialization = validated_data.pop('specialization')
        doc = Doctor.objects.create(**validated_data,specialization=specialization)

        return doc

    
    
    def get_image(self,obj):
        request = self.context['request']
        return request.build_absolute_uri('media/' + obj.image)


class DoctorWriteSerializer(ModelSerializer):

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
        extra_kwargs = {'ticket': {'required': False}}