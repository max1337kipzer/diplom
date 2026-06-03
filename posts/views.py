from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Post, Comment, Subscription, Notification

User = get_user_model()


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        parent_id = request.POST.get('parent')
        
        if text:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                text=text,
                parent_id=parent_id if parent_id else None
            )
            messages.success(request, 'Комментарий добавлен')
            
            if request.user != post.author:
                Notification.objects.create(
                    user=post.author,
                    notification_type='comment',
                    text=f'{request.user.username} прокомментировал ваш пост "{post.title[:50]}"'
                )
        else:
            messages.error(request, 'Текст не может быть пустым')
    
    return redirect('car_detail', car_id=post.car.id)


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.info(request, 'Лайк убран')
    else:
        post.likes.add(request.user)
        messages.success(request, 'Лайк поставлен')
        
        if request.user != post.author:
            Notification.objects.create(
                user=post.author,
                notification_type='like',
                text=f'{request.user.username} лайкнул ваш пост "{post.title[:50]}"'
            )
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def toggle_subscription(request, user_id):
    subscribed_to = get_object_or_404(User, id=user_id)
    
    if request.user == subscribed_to:
        messages.error(request, 'Нельзя подписаться на самого себя')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    subscription = Subscription.objects.filter(subscriber=request.user, subscribed_to=subscribed_to)
    
    if subscription.exists():
        subscription.delete()
        messages.info(request, f'Вы отписались от {subscribed_to.username}')
    else:
        Subscription.objects.create(subscriber=request.user, subscribed_to=subscribed_to)
        messages.success(request, f'Вы подписались на {subscribed_to.username}')
        
        Notification.objects.create(
            user=subscribed_to,
            notification_type='subscription',
            text=f'{request.user.username} подписался на вас'
        )
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def like_review(request, review_id):
    from garage.models import Review
    review = get_object_or_404(Review, id=review_id)
    
    if request.user in review.likes.all():
        review.likes.remove(request.user)
        messages.info(request, 'Лайк убран')
    else:
        review.likes.add(request.user)
        messages.success(request, 'Лайк поставлен')
    
    return redirect('car_detail', car_id=review.car.id)


@login_required
def feed(request):
    subscribed_users = request.user.subscriptions_out.values_list('subscribed_to', flat=True)
    posts = Post.objects.filter(author__id__in=subscribed_users).order_by('-created_at')
    return render(request, 'posts/feed.html', {'posts': posts})


@login_required
def notifications(request):
    notifications_list = request.user.notifications.order_by('-created_at')
    notifications_list.update(is_read=True)
    return render(request, 'posts/notifications.html', {'notifications': notifications_list})