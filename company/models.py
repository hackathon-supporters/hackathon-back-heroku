from django.db import models
import uuid as uuid_lib
from django.conf import settings

# Create your models here.
class Company(models.Model):
    id = models.UUIDField(primary_key=True,verbose_name='id',default=uuid_lib.uuid4,editable=False,unique=True)
    companyname = models.TextField(verbose_name='社名')
    logourl = models.URLField(max_length=512,default="")

    def get_id(self):
        return str(self.id)
    
    def get_companyname(self):
        return str(self.companyname)

    def get_logo(self):
        return str(self.logourl)