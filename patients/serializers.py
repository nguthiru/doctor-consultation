from rest_framework.serializers import ModelSerializer
from .models import *

class PatientSerializer(ModelSerializer):

    class Meta:
        model = Patient
        fields = "__all__"
        extra_kwargs = {'user': {'required': False}}