from django.urls import path,include
from .views import *

urlpatterns=[
    path('',Companies.as_view(),name='companies'),
    path('company',getCompanyQuiter.as_view(),name='companyquiter'),
]