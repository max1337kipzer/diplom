from django.contrib import admin
from .models import Post, Comment, Subscription, Notification


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'text', 'created_at', 'parent')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username', 'post__title')
    list_display_links = ('id', 'text')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed_to', 'created_at')
    search_fields = ('subscriber__username', 'subscribed_to__username')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'text', 'is_read', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('notification_type', 'is_read', 'created_at')