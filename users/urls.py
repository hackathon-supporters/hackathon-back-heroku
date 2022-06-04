from django.urls import path,include
from .views import *

urlpatterns=[
    path('signup',UserRegister.as_view(),name='register'),
    path('signin',UserLogin.as_view(),name='siginin'),
]