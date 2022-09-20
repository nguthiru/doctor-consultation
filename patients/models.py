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
        return self.user

