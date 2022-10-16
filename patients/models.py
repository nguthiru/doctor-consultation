from django.db import models
from django.contrib.auth import get_user_model

User= get_user_model()
# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateTimeField()
    phone_number = models.CharField(max_length=15,unique=True)
    address = models.TextField()

    def __str__(self) -> str:
        return self.user.username

class Application(models.Model):

    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey("doctors.Doctor",on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return self.patient.first_name

class Ticket(models.Model):
    application = models.ForeignKey(Application,on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    payment_identifier = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

class TicketMedia(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    file = models.FileField(max_length=300)
    date_shared = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    caption = models.TextField(null=True)
