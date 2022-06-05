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
        student.user_id as student,
        society.user_id as society,
        chat_chatroomstate.state
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
            student_id = row[1]
            society_id = row[2]
            state = row[3]
            roomlist.append({
                "room_id":room_id,
                "student_id":student_id,
                "society_id":society_id,
                "state":state,
            })
        
        context = {
            "ChatRoom":roomlist
        }

        return Response(context,status=status.HTTP_200_OK)

class ChatRoom(APIView):

    def get(self,request,format=None):
        user = checktoken(token=request.META.get('HTTP_AUTHORIZATION'))
        if user == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        room_id = request.GET.get("roomid")
        #print(room_id)
        if room_id == None:
            return Response({"message":"room_id is not"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room = ChatroomState.objects.get(room_id = room_id)
            if room.state != 2:
                return Response({"message":"this room is not open"},status=status.HTTP_400_BAD_REQUEST)
            chatobjs = Chatlog.objects.filter(room = room).order_by('created_at').values()
        except Exception as e:
            print(e)

        context = {
            "room_id":room_id,
            "chat":chatobjs,
        }

        return Response(context,status=status.HTTP_200_OK)

    def post(self,request,format=None):
        """
        chatを送る
        room_idで特定
        user_idで社会人かどうか
        testももらう
        """
        user = checktoken(token=request.META.get('HTTP_AUTHORIZATION'))
        if user == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        print(user)
        print(request.data)
        room_id = request.data.get('roomid')
        text = request.data.get('text')

        if room_id == None or \
            text == None:
            return Response({"message":"情報足りない pls send roomid and text"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room = ChatroomState.objects.get(room_id = room_id)
            if room.state == False:
                return Response({"message":"this room is not open"},status=status.HTTP_400_BAD_REQUEST)
            userid = str(user.id).replace("-","")
            com = f'''
            select humanprofile_humanprofile.society_or_student from humanprofile_humanprofile 
            where humanprofile_humanprofile.user_id = '{userid}'
            '''
            cursor = connection.cursor()
            cursor.execute(com)
            onoff = True if cursor.fetchall()[0][0] == 1 else False

        except Exception as e:
            print(e)
        
        Chatlog.objects.create(room = room,text = text,society_or_student = onoff)
        return Response({"text":text},status.HTTP_201_CREATED)