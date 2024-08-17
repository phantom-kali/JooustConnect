from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "is_read", "timestamp")
    search_fields = ("user__username", "content")
    list_filter = ("is_read", "timestamp")
    ordering = ("-timestamp",)
