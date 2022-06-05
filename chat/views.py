from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from humanprofile.models import Humanprofile
from users.models import User
from django.db import transaction,connection

from .models import ChatroomState,Chatlog
from users.backends import checktoken
#from .serializer import ChatroomState
# Create your views here.

class ChatRequest(APIView):
    #permission_classes = (permissions.AllowAny)
    def post(self,request,format=None):
        """
        リクエスト飛ばす
        待ち状態を返却 つまり 1 -> 1で成功
        """
        student = checktoken(token=request.META.get('HTTP_AUTHORIZATION'))
        if student == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        society_id = request.data.get('user_id')
        if society_id == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        society = User.objects.get(id = society_id)
        soc_pro = Humanprofile.objects.get(user=society)

        if not soc_pro.society_or_student:
            """
            実は社会人のidが送られてなかった
            弾け！
            """
            return Response(status=status.HTTP_400_BAD_REQUEST)
        state_goc = ChatroomState.objects.get_or_create(
                                            student_user = student,
                                            society_user = society)
        context = {
            "status":state_goc[0].state,
            "message": 'リクエストを送信しました' if state_goc[1] else 'そのリクエストは送信済みです'
        }

        return Response(context,status=status.HTTP_201_CREATED)


class ChatRooms(APIView):
    #permission_classes = (permissions.AllowAny)
    def get(self,request,format=None):
        """
        userが所属しているルームを取ってきて
        ルームidの配列を返す
        """
        user = checktoken(token=request.META.get('HTTP_AUTHORIZATION'))
        if user == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        cursor = connection.cursor()
        userid = str(user.id).replace("-","")
        com = f'''
        select chat_chatroomstate.room_id,
        student.username as student,
        society.username as society
        from chat_chatroomstate
        join humanprofile_humanprofile as student 
        on student.user_id = chat_chatroomstate.student_user_id 
        join humanprofile_humanprofile as society 
        on society.user_id = chat_chatroomstate.society_user_id
        where student_user_id = '{userid}' OR society_user_id = '{userid}'
        '''
        print(com)
        cursor.execute(com)
        rows = cursor.fetchall()
        roomlist = list()
        for row in rows:
            room_id = row[0]
            student_name = row[1]
            society_name = row[2]
            roomlist.append({
                "room_id":room_id,
                "student_name":student_name,
                "society_name":society_name
            })
        
        context = {
            "ChatRoom":roomlist
        }

        return Response(context,status=status.HTTP_200_OK)

class ChatRoom(APIView):

    def get(self,request,format=None):
        pass

    def post(self,request,format=None):
        pass