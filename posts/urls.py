from django.urls import path
from . import views

urlpatterns = [
    path('comment/<int:post_id>/add/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('review/<int:review_id>/like/', views.like_review, name='like_review'),
    path('subscribe/<int:user_id>/', views.toggle_subscription, name='toggle_subscription'),
    path('feed/', views.feed, name='feed'),
    path('notifications/', views.notifications, name='notifications'),
]