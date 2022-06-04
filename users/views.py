from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from rest_framework import authentication, permissions, generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView

from .backends import EmailAuthBackend, maketoken
from .serializer import UserSerializer
from .models import User,UserManager,Token
# Create your views here.

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @transaction.atomic
    def post(self,request,format = None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    serializer_class = UserSerializer
    def post(self,request,format=None):
        email = request.data["email"]
        password = request.data["password"]
        if email == None and \
            password == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        eab = EmailAuthBackend()
        userobj = EmailAuthBackend.authenticate(eab,request=request,email=email,password=password)
        if userobj == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token = maketoken(email,password,userobj)
        return Response({"token":token},
            status = status.HTTP_200_OK)