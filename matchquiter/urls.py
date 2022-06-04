from django.urls import path,include
from .views import *

urlpatterns=[
    path('',HelloWorld.as_view(),name='hello'),
]