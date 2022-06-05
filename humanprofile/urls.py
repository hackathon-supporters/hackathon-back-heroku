from django.urls import path,include
from .views import *

urlpatterns=[
    path('',ProfileChange.as_view(),name='register'),
    path('who',getProfilebyId.as_view()),
]