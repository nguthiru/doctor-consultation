from rest_framework.serializers import ModelSerializer,SerializerMethodField
from django.contrib.auth import get_user_model

from django.contrib.auth import get_user_model
from doctors.models import Doctor

from doctors.serializers import DoctorSerializer
from patients.models import Patient
class UserSerializer(ModelSerializer):

    profile = SerializerMethodField('get_profile')
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name','is_doctor','profile')

    def get_profile(self,obj):
        from patients.serializers import PatientSerializer

        if obj.is_doctor:
            doctor = Doctor.objects.get(user=obj)
            return DoctorSerializer(doctor).data
        else:
            patient = Patient.objects.get(user=obj)
            return PatientSerializer(patient).data