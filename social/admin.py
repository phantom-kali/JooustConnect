from django.contrib import admin
from .models import Post, PostView, Comment, Report


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "created_at", "n_views", "n_likes")
    search_fields = ("user__username", "content")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "viewed_at")
    search_fields = ("post__content", "user__username")
    list_filter = ("viewed_at",)
    ordering = ("-viewed_at",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("reporter", "post", "report_type", "created_at", "is_resolved")
    list_filter = ("report_type", "is_resolved", "created_at")
    search_fields = ("reporter__username", "post__content", "description")
    actions = ["mark_resolved"]

    def mark_resolved(self, request, queryset):
        queryset.update(is_resolved=True)

    mark_resolved.short_description = "Mark selected reports as resolved"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "content", "created_at")
    search_fields = ("post__content", "user__username", "content")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
