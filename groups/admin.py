from django.contrib import admin
from .models import Group, GroupPost, GroupMessage


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name", "description")
    list_filter = ("created_at",)
    ordering = ("name",)


@admin.register(GroupPost)
class GroupPostAdmin(admin.ModelAdmin):
    list_display = ("group", "user", "content", "created_at", "n_views", "get_n_likes")
    search_fields = ("group__name", "user__username", "content")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    def get_n_likes(self, obj):
        return obj.n_likes

    get_n_likes.short_description = "Number of Likes"


@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ("group", "sender", "content", "timestamp")
    search_fields = ("group__name", "sender__username", "content")
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)
