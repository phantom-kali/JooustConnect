from django.contrib import admin
from .models import Message

<<<<<<< HEAD

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "content", "timestamp")
    search_fields = ("sender__username", "receiver__username", "content")
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)
=======
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
