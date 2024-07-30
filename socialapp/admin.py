from django.contrib import admin
from .models import User, Post, PostView, Comment, Group, GroupPost, GroupMessage, Message, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'email', 'course', 'year', 'profile_picture')
    search_fields = ('username', 'nickname', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at', 'n_views', 'n_likes')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'viewed_at')
    search_fields = ('post__content', 'user__username')
    list_filter = ('viewed_at',)
    ordering = ('-viewed_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_at')
    search_fields = ('post__content', 'user__username', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('name',)

@admin.register(GroupPost)
class GroupPostAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'content', 'created_at', 'n_views', 'get_n_likes')
    search_fields = ('group__name', 'user__username', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    def get_n_likes(self, obj):
        return obj.n_likes
    get_n_likes.short_description = 'Number of Likes'

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('group', 'sender', 'content', 'timestamp')
    search_fields = ('group__name', 'sender__username', 'content')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'is_read', 'timestamp')
    search_fields = ('user__username', 'content')
    list_filter = ('is_read', 'timestamp')
    ordering = ('-timestamp',)
