from django.db import models
from django.conf import settings
from garage.models import Car


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', related_name='posts')
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автомобиль', related_name='posts')
    image = models.ImageField('Изображение', upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_posts', verbose_name='Лайки')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.author.username}'

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments')
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ответ на', related_name='replies')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        if self.parent:
            return f'Ответ от {self.author.username} на комментарий {self.parent.author.username}'
        return f'Комментарий от {self.author.username} к {self.post.title}'


class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Подписчик', related_name='subscriptions_out')
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', related_name='subscriptions_in')
    created_at = models.DateTimeField('Дата подписки', auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('subscriber', 'subscribed_to')

    def __str__(self):
        return f'{self.subscriber.username} подписан на {self.subscribed_to.username}'


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('comment', 'Комментарий'),
        ('like', 'Лайк'),
        ('subscription', 'Подписка'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='notifications')
    notification_type = models.CharField('Тип уведомления', max_length=20, choices=NOTIFICATION_TYPES)
    text = models.CharField('Текст уведомления', max_length=255)
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.text[:50]}'