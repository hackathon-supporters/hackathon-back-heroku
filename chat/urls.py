from django.urls import path,include
from .views import *

urlpatterns=[
    path('request',ChatRequest.as_view()),
    path('chat-rooms',ChatRooms.as_view()),
    path('',ChatRoom.as_view())
]