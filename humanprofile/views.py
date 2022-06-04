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
            return Response(status=status.HTTP_400_BAD_REQUEST)
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

        if checktoken(token=request.META.get('HTTP_AUTHORIZATION')) == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        print(request.data)
        id = request.data.get('id')
        username = request.data.get('username')
        faceurl = request.data.get('faceurl')
        society_or_student = request.data.get('society_or_student')

        if username == None or\
            faceurl == None or\
                society_or_student == None or\
                    id == None:
            print(id)
            print(faceurl)
            print(society_or_student)
            print(id)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        profile = Humanprofile.objects.get(id = id)
        profile.username = username
        profile.faceurl = faceurl
        profile.society_or_student = society_or_student
        profile.save()

        user = profile.user
        user.username = username
        user.save()

        return Response({"message":"success"},status=status.HTTP_200_OK)