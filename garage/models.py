from django.db import models
from django.conf import settings


class CarBrand(models.Model):
    name = models.CharField('Название марки', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Марка автомобиля'
        verbose_name_plural = 'Марки автомобилей'

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, verbose_name='Марка', related_name='models')
    name = models.CharField('Название модели', max_length=100)

    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'
        unique_together = ('brand', 'name')

    def __str__(self):
        return f'{self.brand.name} {self.name}'


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('manual', 'Механика'),
        ('automatic', 'Автомат'),
        ('robot', 'Робот'),
        ('cvt', 'Вариатор'),
    ]

    DRIVE_CHOICES = [
        ('front', 'Передний'),
        ('rear', 'Задний'),
        ('full', 'Полный'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', related_name='cars', null=True, blank=True)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, verbose_name='Марка')
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name='Модель')
    year = models.IntegerField('Год выпуска')
    vin = models.CharField('VIN номер', max_length=17, blank=True, null=True)
    license_plate = models.CharField('Госномер', max_length=20, blank=True, null=True)
    color = models.CharField('Цвет', max_length=50, blank=True, null=True)
    engine_volume = models.DecimalField('Объём двигателя (л)', max_digits=3, decimal_places=1, blank=True, null=True)
    horsepower = models.IntegerField('Мощность (л.с.)', blank=True, null=True)
    transmission = models.CharField('Коробка передач', max_length=20, choices=TRANSMISSION_CHOICES, blank=True, null=True)
    drive = models.CharField('Привод', max_length=20, choices=DRIVE_CHOICES, blank=True, null=True)
    photo = models.ImageField('Фото автомобиля', upload_to='cars/', blank=True, null=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.brand.name} {self.model.name} ({self.year})'


class Review(models.Model):
    RATING_CHOICES = [
        (1, '★ 1'),
        (2, '★★ 2'),
        (3, '★★★ 3'),
        (4, '★★★★ 4'),
        (5, '★★★★★ 5'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль', related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', related_name='reviews')
    text = models.TextField('Текст отзыва', max_length=1000)
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES, default=5)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_reviews', verbose_name='Лайки отзыва')
    
    class Meta:
        verbose_name = 'Отзыв об автомобиле'
        verbose_name_plural = 'Отзывы об автомобилях'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Отзыв от {self.author.username} на {self.car.brand.name} {self.car.model.name}'
    
    def total_likes(self):
        return self.likes.count()


class ReviewComment(models.Model):
    """Комментарий к отзыву"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, verbose_name='Отзыв', related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', related_name='review_comments')
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ответ на', related_name='replies')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_review_comments', verbose_name='Лайки')

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзывам'
        ordering = ['created_at']

    def __str__(self):
        if self.parent:
            return f'Ответ от {self.author.username} на комментарий {self.parent.author.username}'
        return f'Комментарий от {self.author.username} к отзыву {self.review.id}'
    
    def total_likes(self):
        return self.likes.count()