from django.contrib import admin
from .models import CarBrand, CarModel, Car
from django.contrib import admin
from .models import CarBrand, CarModel, Car, Review  # Добавь Review сюда

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('owner', 'brand', 'model', 'year')

    from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('car__brand__name', 'car__model__name', 'author__username', 'text')