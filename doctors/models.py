from django.db import models
from django.contrib.auth import get_user_model

from patients.models import Ticket

# Create your models here.
User= get_user_model()


class Specialization(models.Model):
    name = models.CharField(max_length=255)
    consultation_price = models.FloatField(default=1000)

    def __str__(self) -> str:
        return self.name
class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15,unique=True)
    specialization = models.OneToOneField(Specialization,on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return self.user.username
class DoctorImage(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    image = models.ImageField()
class Consultation(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    diagnosis = models.TextField()
    remarks = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    