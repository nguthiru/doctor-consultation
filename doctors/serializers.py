from rest_framework.serializers import ModelSerializer
from .models import *

class DoctorSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Doctor
        extra_kwargs = {'user': {'required': False}}