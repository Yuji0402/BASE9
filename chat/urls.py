from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list_view, name='chat-list'),
    path('<int:pk>/', views.chat_room_view, name='chat-room'),
]
