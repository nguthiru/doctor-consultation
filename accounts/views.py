from rest_framework.authtoken.models import Token
from operator import imod
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user
from rest_framework.response import Response
from accounts.serializers import UserSerializer
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer
from patients.models import Patient
from patients.serializers import PatientSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
USERS = get_user_model()
# Create your views here.


@api_view(['GET'])
def me(request):
    serial = UserSerializer(request.user,context={'request':request})

    return Response(serial.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    password1 = request.data.get("password1")
    password2 = request.data.get("password2")
    email = request.data.get("email")

    if (username == None or password1 == None or password2 == None or email == None):
        return Response("Fill all fields", status=400)
    if password1 != password2:
        return Response("Passwords don't match", status=400)
    else:
        try:
            user = USERS.objects.get(username=username)
            return Response("User already exists", status=400)
        except USERS.DoesNotExist:
            user = USERS.objects.create(username=username, email=email)
            user.set_password(password1)
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            user_ser = UserSerializer(user)
            return Response({"token": token.key, "user": user_ser.data}, status=201)


@api_view(['POST'])
def update_profile(request):
    user = request.user

    if user.is_doctor:
        serializer = DoctorSerializer
        instance = get_object_or_404(Doctor, user=user)
    else:
        serializer = PatientSerializer
        instance = get_object_or_404(Patient, user=user)

    serial = serializer(instance=instance, data=request.data, partial=True)
    if serial.is_valid():
        serial.save()
        return Response(serial.data,)
    else:
        return Response(serial.errors)
