from django.contrib import admin

# Register your models here.
# from .models import Message  

# admin.site.register(Message)
# admin.site.register(Conversation)\


from .models import Thread, ChatMessage

class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread 


admin.site.register(Thread, ThreadAdmin)