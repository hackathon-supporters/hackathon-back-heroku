from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from humanprofile.models import Humanhistory, Humanprofile
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
        """
        company id -> 退職者 -> その退職者の経歴
        """
        print(request)
        user = checktoken(request.META.get('HTTP_AUTHORIZATION'))
        if user == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        company_id = request.GET.get('company_id')
        if company_id == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        company = Company.objects.get(id = company_id)
        quithumans = getQuiter(company)
        print(quithumans)
        print(type(quithumans))

        context = {
            "profiles":getprofiles(quithumans)
        }

        return Response(context,status.HTTP_200_OK)

def getQuiter(company:Company):
    quithumans = set()
    soc_humans = Humanhistory.objects.filter(company=company)
    for human in soc_humans:
        quithumans.add(human.user)
    """
    認証userモデル
    """
    return quithumans

def getprofiles(humanlist:set):
    """
    認証userモデルが来る
    """
    profilelist = list()
    for human in humanlist:
        profilelist.append(getprofile(human))
    return profilelist

def getprofile(human:User):
    quitcompanies = Humanhistory.objects.filter(user=human).values_list('company',flat=True)
    quitcompaniesprofile = Humanprofile.objects.get(user=human)
    dictiona = {
        "id":human.id,
        "name":quitcompaniesprofile.username,
        "avater":quitcompaniesprofile.faceurl,
        "society_or_student":quitcompaniesprofile.society_or_student,
        "histories":quitcompanies
    }
    return dictiona