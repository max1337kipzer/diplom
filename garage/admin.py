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
    list_display = (
        'id', 'owner', 'brand', 'model', 'year', 'color', 'engine_volume', 
        'horsepower', 'transmission', 'drive', 'body_type', 'fuel_type',
        'acceleration', 'top_speed', 'fuel_consumption', 'trunk_volume',
        'length', 'width', 'height', 'weight', 'license_plate', 'vin'
    )
    list_filter = (
        'brand', 'year', 'transmission', 'drive', 'body_type', 'fuel_type'
    )
    search_fields = (
        'owner__username', 'brand__name', 'model__name', 'vin', 'license_plate'
    )
    list_editable = ('color', 'engine_volume', 'horsepower')
    list_per_page = 20
    fieldsets = (
        ('Владелец и идентификация', {
            'fields': ('owner', 'brand', 'model', 'year', 'vin', 'license_plate')
        }),
        ('Внешний вид', {
            'fields': ('color', 'body_type', 'photo')
        }),
        ('Двигатель и трансмиссия', {
            'fields': ('engine_volume', 'horsepower', 'fuel_type', 'transmission', 'drive')
        }),
        ('Динамика и расход', {
            'fields': ('acceleration', 'top_speed', 'fuel_consumption')
        }),
        ('Габариты и масса', {
            'fields': ('length', 'width', 'height', 'weight', 'trunk_volume')
        }),
    )


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