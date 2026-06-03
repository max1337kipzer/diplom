from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Расширенная модель пользователя.
    AbstractUser уже содержит: username, email, first_name, last_name, password, is_active и т.д.
    """
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    city = models.CharField('Город', max_length=100, blank=True, null=True)
    bio = models.TextField('О себе', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username