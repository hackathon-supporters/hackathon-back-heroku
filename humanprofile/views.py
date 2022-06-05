from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from users.models import User
from django.db import transaction

from .models import Humanprofile
from users.backends import checktoken
from .serializer import HumanprofileSerializer
# Create your views here.

class ProfileChange(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = HumanprofileSerializer
    def get(self,request,format=None):
        #print("hello")
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        user = checktoken(token=token)
        if user == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        humanprofile = Humanprofile.objects.get_or_create(user=user)[0]
        #print(str(humanprofile))
        context = {
            "id":str(humanprofile.id),
            "faceurl":str(humanprofile.faceurl),
            "username":humanprofile.user.username,
            "sos":humanprofile.society_or_student,
        }
        return Response(context,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):

        user = checktoken(token=request.META.get('HTTP_AUTHORIZATION'))
        if user == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        print(request.data)
        #id = request.data.get('id')
        username = request.data.get('username')
        faceurl = request.data.get('faceurl')
        society_or_student = request.data.get('society_or_student')

        if username == None or\
            faceurl == None or\
                society_or_student == None:
                    #id == None
            print(username)
            print(faceurl)
            print(society_or_student)
            #print(id)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        profile = Humanprofile.objects.get(user = user)
        profile.username = username
        profile.faceurl = faceurl
        profile.society_or_student = society_or_student
        profile.save()

        user = profile.user
        user.username = username
        user.save()

        return Response({"message":"success"},status=status.HTTP_201_CREATED)

class getProfilebyId(APIView):
    def get(self,request,format=None):
        user = checktoken(token=request.META.get('HTTP_AUTHORIZATION'))
        if user == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        take_user_id = request.GET.get('user_id')
        if take_user_id == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        take_user = User.objects.get(id = take_user_id)
        take_user_pro = Humanprofile.objects.get(user=take_user)

        context = {
            "id":take_user.id,
            "name":take_user_pro.username,
            "avatar":take_user_pro.faceurl,
            "society_or_student":take_user_pro.society_or_student,
            "histories":"",
        }

        return Response(context,status=status.HTTP_200_OK)