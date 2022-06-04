from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from .models import User,UserManager

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)

    class Meta:
        model = User
        fields = ('id','email','password')
    
    def create(self,validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        return User.objects.create_user(email = email,password = password)