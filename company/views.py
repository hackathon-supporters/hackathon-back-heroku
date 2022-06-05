from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from users.models import User
from django.db import transaction

from .models import Company
from users.backends import checktoken

class Companies(APIView):
    def get(self,request,format=None):
        user = checktoken(request.META.get('HTTP_AUTHORIZATION'))
        if user == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        companies = Company.objects.all().values()
        #for company in companies:
        context = companies

        return Response(context,status.HTTP_200_OK)
