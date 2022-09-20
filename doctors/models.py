from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User= get_user_model()

class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15,unique=True)

    def __str__(self) -> str:
        return self.user
