from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='chat_rooms', verbose_name='参加者'
    )
    name = models.CharField('ルーム名', max_length=100, blank=True)
    match_post = models.ForeignKey(
        'matches.MatchPost', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='chat_rooms'
    )
    recruit_post = models.ForeignKey(
        'recruitment.RecruitPost', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='chat_rooms'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f'Room #{self.pk}'

    def get_last_message(self):
        return self.messages.order_by('-created_at').first()

    def get_unread_count(self, user):
        return self.messages.exclude(sender=user).filter(is_read=False).count()


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )
    content = models.TextField('内容')
    is_read = models.BooleanField('既読', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username}: {self.content[:30]}'
