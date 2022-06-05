from django.db import models
import uuid as uuid_lib
from django.conf  import settings

# Create your models here.
class ChatroomState(models.Model):
    room_id = models.UUIDField(primary_key=True,verbose_name='room_id',default=uuid_lib.uuid4,editable=False,unique=True)
    student_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        verbose_name="studnet",
                                        on_delete=models.CASCADE,
                                        related_name='studnet')
    society_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        verbose_name="society",
                                        on_delete=models.CASCADE,
                                        related_name="society")
    state = models.PositiveSmallIntegerField(default=1,verbose_name='承認ステータス',help_text='0:拒否,1:待ち,2:許可')

    def __str__(self):
        return f'{self.student_user}-{self.society_user}'

class Chatlog(models.Model):
    room = models.ForeignKey(ChatroomState,
                                    on_delete=models.CASCADE,
                                    verbose_name="room_id")
    text = models.TextField(verbose_name='chattext')
    society_or_student = models.BooleanField(help_text='社会人か就活生か',default=False)
    created_at = models.DateTimeField("投稿日",auto_now_add=True)