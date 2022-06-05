from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from humanprofile.models import Humanhistory
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

class getCompanyQuiter(APIView):
    def get(self,request,format=None):
        user = checktoken(request.META.get('HTTP_AUTHORIZATION'))
        if user == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        company_id = request.GET.get('company_id')
        if company_id == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        company = Company.objects.get(id = company_id)
        soc_humans = Humanhistory.objects.filter(company = company)
        soc_lsit = list()
        for human in soc_humans:
            soc_lsit.append(human.user)
        
        context = {
            "users":soc_lsit,
        }

        return Response(context,status.HTTP_200_OK)
