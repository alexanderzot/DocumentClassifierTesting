from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from .models import *
from .serializers import *


@api_view(['POST'])
def user_sign_in(request):
    data = request.data
    email = ("email" in data) and data.get("email") or None
    email = email.lower()
    password = ("password" in data) and data.get("password") or None

    if not User.objects.filter(email=email).exists():
        return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'FAIL'})

    username = User.objects.get(email=email).username
    auth_user = auth.authenticate(username=username, password=password)

    if not auth_user:
        return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'FAIL'})

    auth.login(request, auth_user)
    username = str(auth_user)
    return Response(status=status.HTTP_200_OK, data={'status': 'OK', 'username': username})


@api_view(['POST'])
def user_sign_out(request):
    user = auth.get_user(request)

    if not user.is_authenticated:
        return Response(status=status.HTTP_204_NO_CONTENT, data={'status': 'FAIL'})

    auth.logout(request)
    return Response(status=status.HTTP_200_OK, data={'status': 'OK'})


@api_view(['POST'])
def user_sign_up(request):
    data = request.data
    email = ("email" in data) and data.get("email") or None
    password1 = ("password1" in data) and data.get("password1") or None
    password2 = ("password2" in data) and data.get("password2") or None

    if password1 != password2:
        return Response(status=status.HTTP_200_OK, data={'status': 'FAIL', 'msg': 'Пароли не совпадают!'})
    if User.objects.filter(email=email).exists():
        return Response(status=status.HTTP_200_OK, data={'status': 'FAIL', 'msg': 'Почта уже зарегистрирована!'})

    User.objects.create_user(username=email.lower(), email=email, password=password1)
    return Response(status=status.HTTP_200_OK,
                    data={
                        'status': 'OK',
                        'msg': 'Регистрация успешна завершена! Автоматическое перенаправление.'
                    })


class ListFileView(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class DetailFileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

