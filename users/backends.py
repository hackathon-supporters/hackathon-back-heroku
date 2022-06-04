from django.contrib.auth.backends import ModelBackend
from .models import User,Token
from MatchQuiter.settings import SECRET_KEY
import hashlib


class EmailAuthBackend(ModelBackend):
    def __init__(self):
        super().__init__()
    def authenticate(self,request,email=None,password=None,**kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password) and \
                self.user_can_authenticate(user):
                return user

def maketoken(email:str,password:str,user:User):
    secret_key = SECRET_KEY
    seed = 0
    
    while(True):
        seed = seed+100
        summarystring = str(email+secret_key+password) +str(seed)
        print(summarystring)
        print(type(summarystring))
        hash512string = hashlib.sha512(summarystring.encode('utf-8')).hexdigest()
        if len(Token.objects.filter(token=hash512string)) == 0:
            break
    
    token = Token.objects.create(user=user,token = hash512string)
    return token.token

def checktoken(token):
    """
    return user or None
    """
    try:
        user = Token.objects.get(token=token).user
    except Token.DoesNotExist:
        return None
    return user