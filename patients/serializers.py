from django.forms import URLField
from rest_framework.serializers import ModelSerializer,SerializerMethodField


from .models import *
from doctors.serializers import DoctorSerializer
from doctors.models import Doctor
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

class TicketMediaSerializer(ModelSerializer):
    # file = SerializerMethodField('get_file_url')
    sender = UserSerializer(read_only=True)
    class Meta:
        model = TicketMedia
        fields = '__all__'
        extra_kwargs = {'sender':{'required':False}}

    def get_file_url(self,obj):
         return self.context['request'].build_absolute_uri(obj.file)