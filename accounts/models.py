from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    USERNAME_FIELD = 'username'
    is_doctor = models.BooleanField(default=False)

