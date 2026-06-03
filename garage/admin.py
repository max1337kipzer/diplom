from django.contrib import admin
from .models import CarBrand, CarModel, Car, Review, ReviewComment


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name')
    search_fields = ('name',)
    list_filter = ('brand',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('owner', 'brand', 'model', 'year', 'license_plate')
    search_fields = ('owner__username', 'vin', 'license_plate')
    list_filter = ('brand', 'year', 'transmission', 'drive')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('car__brand__name', 'car__model__name', 'author__username', 'text')


@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'created_at', 'parent')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username')