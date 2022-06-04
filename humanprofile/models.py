from django.db import models
import uuid as uuid_lib
from django.conf import settings

# Create your models here.
class Humanprofile(models.Model):
    id = models.UUIDField(primary_key=True,verbose_name='id',default=uuid_lib.uuid4,editable=False,unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="user",on_delete=models.CASCADE)
    username = models.CharField(max_length=30,unique=False,default="")
    faceurl = models.URLField(verbose_name='faceurl',max_length=512,default="")
    society_or_student = models.BooleanField(help_text='社会人か就活生か',default=False)
    """
    社会人:True
    生徒:False
    """
    def __str__(self):
        return self.user.email