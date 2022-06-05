from django.urls import path,include
from .views import *

urlpatterns=[
    path('',Companies.as_view(),name='register'),
    
]