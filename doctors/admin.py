from django.contrib import admin
from .models import Doctor, Specialization
# Register your models here.
admin.site.register([Doctor,Specialization])