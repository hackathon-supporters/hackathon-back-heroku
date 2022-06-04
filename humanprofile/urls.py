from django.urls import path,include
from .views import *

urlpatterns=[
    path('',ProfileChange.as_view(),name='register'),
]
""" <uuid:profile_id>/ """