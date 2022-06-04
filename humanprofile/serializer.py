from rest_framework import serializers
from .models import Humanprofile

class HumanprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Humanprofile
        fields = ('id','username','faceurl','society_or_student',)