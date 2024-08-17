from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ("user", "content", "is_read", "timestamp")
    search_fields = ("user__username", "content")
    list_filter = ("is_read", "timestamp")
    ordering = ("-timestamp",)
=======
    list_display = ('user', 'content', 'is_read', 'timestamp')
    search_fields = ('user__username', 'content')
    list_filter = ('is_read', 'timestamp')
    ordering = ('-timestamp',)

>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
