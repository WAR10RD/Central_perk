# # chat/urls.py
# from django.urls import path

# from . import views

# urlpatterns = [
#     # path('', views.create_room, name='create_room'),
#      # path('<str:room_name>/', views.room, name='room'),
#     # path('chat', views.chat_view, name='chats'),
#     # path('chat/<int:sender>/<int:receiver>', views.message_view, name='chat'),
#     # path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
#     # path('api/messages', views.message_list, name='message-list'),
# ]

from django.urls import path, re_path

from . import views
from .views import ThreadView, InboxView
import chat

app_name = 'chat'
urlpatterns = [
    path("", InboxView.as_view()),
    re_path(r"^(?P<username>[\w.@+-]+)", ThreadView.as_view()),
]
