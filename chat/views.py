from django.contrib.auth.models import User
from django.shortcuts import render ,redirect
from django.utils.safestring import mark_safe
import json
from django.http.response import JsonResponse, HttpResponse
# from rest_framework.parsers import JSONParser
# from .models import Message
# from chat.serializers import MessageSerializer
# Create your views here.
# chat/views.py
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden, request
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.views.generic import DetailView, ListView

from .form import ComposeForm
from .models import Thread, ChatMessage

class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            query = Thread.objects.by_user(self.request.user)
            # print("query is ",query)
            querys = Thread.objects.get_users_message(self.request.user)
            print("querys is ",querys)
            
            user_id = self.request.user.id
            message_data_list = []
            
            print("user id is ",user_id)

            if querys:
                for i in querys:
                    # print("in i",i)
                    if i.first == self.request.user:
                        other_user = i.second
                    else:
                        other_user = i.first
                        print("first user ",i.first)
                        print("second user ",i.second)
                    print(type(other_user),other_user)

                    chat = ChatMessage.objects.filter(thread=i.id).order_by('-timestamp').first()
                    # sender_name = User.objects.filter(id=chat[0]['user_id']).values()
                    # print("sender is ",sender_name[0]['username'])
                    # print("message is ",chat[0]['message'])
                    message_data_dict = {}
                    if chat:
                        sender = chat.user
                        message = chat.message
                        message_data_dict['sender'] = sender
                        message_data_dict['message'] = message
                        message_data_dict['other_user'] = other_user
                    # print("user in chat is ",sender)
                    # print("chat is ",message)
                    
                    # for i in chat:
                        # print("i is ",i.message)
                    # print(type(sender_name[0]['username']))
                    
                    
                    message_data_list.append(message_data_dict)
                # print("chat is ",chat)
            # chat = ChatMessage.objects.filter(thread=querys.id).values().order_by('-timestamp')
            # print("chat is ",chat)
            print("messages are ",message_data_list)
            # self.x = self.get_object()
            # print("querys is ",querys.first)
            # print("querys is ",querys.second)
            return message_data_list
        else:
            message_data_list=[]
            return message_data_list
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        # print("data is ",data)
        return data

    # def get_object(self):
    #     other_username  = self.kwargs.get("username")
    #     print("other username is :",other_username)
    #     obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
    #     if obj == None:
    #         raise Http404
    #     return obj

class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = '#'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        print("other username is :",other_username)
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        print("in thread contsext ,",context)
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)
        # return render(request, "feed/search_posts.html", {})


# def messages(request):
	
# 	print("in the messages")
	
# 	return render(request, 'chat/inbox.html', {})
# @csrf_exempt
# def message_list(request, sender=None, receiver=None):
#     """
#     List all required messages, or create a new message.
#     """
#     if request.method == 'GET':
#         messages = Message.objects.filter(sender_id=sender, receiver_id=receiver)
#         serializer = MessageSerializer(messages, many=True, context={'request': request})
#         for message in messages:
#             # message.is_read = True
#             message.save()
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = MessageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# def chat_view(request):
#     if not request.user.is_authenticated:
#         return redirect('index')
#     if request.method == "GET":
#         return render(request, 'chat/chat.html',
#                       {'users': User.objects.exclude(username=request.user.username)})


# def message_view(request, sender, receiver):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     if request.method == "GET":
#         return render(request, "chat/messages.html",
#                       {'users': User.objects.exclude(username=request.user.username),
#                        'receiver': User.objects.get(id=receiver),
#                        'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
#                                    Message.objects.filter(sender_id=receiver, receiver_id=sender)})

# def create_room(request):
#     return render(request, 'chat/create_room.html')

# def room(request, room_name):
    
#     recipient = room_name
#     print("room is :",recipient)
#     return render(request, 'chat/room.html', {
#         'room_name': room_name,
#         'recipient':recipient,
#         'username': request.user.username,
#         # 'profile_pic': request.user.profile.image.url,
#     })


# 'room_name_json': mark_safe(json.dumps(room_name)),
#         'username': mark_safe(json.dumps(request.user.username)),






# def get_queryset(self):
#         return Thread.objects.by_user(self.request.user)

#     def get_context_data(self, **kwargs):
#         context = super(InboxView, self).get_context_data(**kwargs)
#         # context['message_list'] = context['foo_list'].filter(Country=64)
#         context['thread']= Thread.objects.filter(Q(first=self.request.user)|Q(second=self.request.user)).values()
        
#         context['messages'] = Thread.objects.by_user(self.request.user)
#         print("context is ",context['thread'])

#         for i in context['messages']:
            
            
#             # print("chat is ",chat)
#             print("in the thread",i)
            
#         # other_user = []
#         # for i in context['thread']:
#         #     print("thread is ",i)
#         #     if i['first_id'] == self.request.user.id:
#         #         username = User.objects.filter(id = i['second_id'])
#         #         other_user.append(username)
#         #     else:
                
#         #         username = User.objects.filter(id = i['first_id'])
#         #         other_user.append(username)
#         # # print("thread obj is ",context['thread'])
#         # print("the other user is ",other_user)
#         thread_obj = []
#         for i in context['messages']:
#             chat = ChatMessage.objects.filter(thread=i).order_by('-timestamp')
            
#             # print("chat is ",chat)
#             context['chat'] = chat[0]
#             thread_obj.append(chat[0])
#             print("chat is user",chat[0])
#             # print("chat is message",chat[0]['message'])
#         # context['messages']= ChatMessage.objects.filter(user=self.request.user)
#         # print("get_context_data ",thread_obj)
#         context['thread_obj']=thread_obj
#         # context['users']=other_user
#         return context
