# # chat/consumers.py
from channels.db import database_sync_to_async
from chat.models import Thread ,ChatMessage
import json , asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        # Join room group
        print("it's alive")
        
        
        self.other_user =  self.scope['url_route']['kwargs']['username']
        
        # print("in the goruup",self.room_group_name)
        me = self.scope['user']
    
        thread_obj = await self.get_thread(me,self.other_user)
        self.thread_obj=thread_obj
        
        print(self.other_user,me)
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.accept()
        
        
    async def disconnect(self, close_code):
        # Leave room group
        print("it's dead ")

    async def websocket_receive(self, events):
        print("in the reicver",events)
        front_text = events.get('text',None)
        print("front",front_text)
        if front_text is not None:
            dict_data = json.loads(front_text)
            print("hello")
            msg = dict_data.get('message')
            print(msg)
            user = self.scope['user']
            me ='default'
            if user.is_authenticated:
                me = user.username
            myResponse = {
                'message':msg,
                'username':me
            }
            await self.create_chat_message(user, msg)
            new_event = json.dumps({
            "type": "websocket.send",
            "text": "helf",
        })
        # broadcast the message
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"chat_message",
                    "text":json.dumps(myResponse)

                }
            )
    @database_sync_to_async
    def get_thread(self, user, other_user):
        # print("thread is ",Thread.objects.get_or_new(user,other_user)[0])
        thread_obj=Thread.objects.get_or_new(user,other_user)[0]
        print("thread is ",thread_obj.second)
        return Thread.objects.get_or_new(user,other_user)[0]

    @database_sync_to_async
    def create_chat_message(self,me,msg):
        thread_obj=self.thread_obj
        # me = self.scope['user']
        return ChatMessage.objects.create(thread=thread_obj,user=me,message=msg)
    async def chat_message(self,event):
        print("message",event)
        await self.send(json.dumps({
            "type":"websocket.send",
            "text":event['text']
        }))

            # await self.send()
        # await self.send({
        #     "type": "websocket.send",
        #     "text": events["text"],
        # })
    # Receive message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     print("in receiver")

    # async def on_open(self, message):
    #     print("in the on_message")
    #     await self.send_json(message)
    # async def websocket_receive(self,event):
    # # async def receive(self, text_data):
    # # #     text_data_json = json.loads(text_data)
    # # #     message = text_data_json['message']
    #     print("in the recieve")
    #     print("in the receive",event)


    
    # # Receive message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

    # # Receive message from room group
    # async def chat_message(self, event):
    #     message = event['message']

    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
# import asyncio
# import json
# from django.contrib.auth import get_user_model
# from channels.consumer import AsyncConsumer
# from channels.db import database_sync_to_async
# from .models import Thread,ChatMessage  

# class ChatConsumer(AsyncConsumer):
#     async def websocket_connect(self,event):
#         print("connected",event)
#         await self.send({
#             "type":"websocket.accept"
#         })
        
    
#     async def websocket_receive(self,event):
#         print("receive",event)
    
#     async def websocket_disconnect(self,event):
#         print("disconnect",event)




# import json
# from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         print("in to the connect")
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         self.send(text_data=json.dumps({
#             'message': message
#         }))



# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))




























# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         })