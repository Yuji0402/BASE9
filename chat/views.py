from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatRoom, Message


@login_required
def chat_list_view(request):
    rooms = request.user.chat_rooms.all().prefetch_related('participants', 'messages')
    return render(request, 'chat/chat_list.html', {'rooms': rooms})


@login_required
def chat_room_view(request, pk):
    room = get_object_or_404(ChatRoom, pk=pk)
    if request.user not in room.participants.all():
        messages.warning(request, 'このチャットルームにアクセスする権限がありません。')
        return redirect('chat-list')
    room.messages.exclude(sender=request.user).update(is_read=True)
    chat_messages = room.messages.select_related('sender').all()
    other_participants = room.participants.exclude(pk=request.user.pk)
    return render(request, 'chat/chat_room.html', {
        'room': room,
        'chat_messages': chat_messages,
        'other_participants': other_participants,
    })
