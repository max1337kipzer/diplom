from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from .models import Car, Review, CarBrand, CarModel, ReviewComment
from .forms import CarForm
from posts.models import Notification
from django.db.models import Q



def car_list(request):
    cars = Car.objects.all()
    return render(request, 'garage/car_list.html', {'cars': cars})


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = car.reviews.all()
    
    if reviews.exists():
        avg_rating = sum(r.rating for r in reviews) / reviews.count()
    else:
        avg_rating = 0
    
    context = {
        'car': car,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'reviews_count': reviews.count(),
    }
    return render(request, 'garage/car_detail.html', context)


@login_required
def add_review(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        
        if text and rating:
            Review.objects.create(
                car=car,
                author=request.user,
                text=text,
                rating=int(rating)
            )
            messages.success(request, 'Отзыв добавлен')
        else:
            messages.error(request, 'Заполните все поля')
        
        return redirect('car_detail', car_id=car.id)
    
    return redirect('car_detail', car_id=car.id)


def search(request):
    """Поиск автомобилей по марке, модели или владельцу"""
    query = request.GET.get('q', '').strip()
    if query:
        cars = Car.objects.filter(
            models.Q(brand__name__icontains=query) |
            models.Q(model__name__icontains=query) |
            models.Q(owner__username__icontains=query)
        ).select_related('brand', 'model', 'owner')
    else:
        cars = Car.objects.none()
    
    context = {
        'cars': cars,
        'query': query,
        'count': cars.count(),
    }
    return render(request, 'garage/search.html', context)


@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            messages.success(request, f'Автомобиль {car.brand.name} {car.model.name} добавлен в гараж')
            return redirect('profile')
        else:
            messages.error(request, 'Ошибка при добавлении автомобиля')
    else:
        form = CarForm()
    
    brands = CarBrand.objects.all()
    return render(request, 'garage/add_car.html', {'form': form, 'brands': brands})


def get_models(request):
    brand_id = request.GET.get('brand_id')
    if brand_id:
        models_list = CarModel.objects.filter(brand_id=brand_id).values('id', 'name')
        return JsonResponse(list(models_list), safe=False)
    return JsonResponse([], safe=False)


@login_required
def add_review_comment(request, review_id):
    """Добавление комментария к отзыву"""
    review = get_object_or_404(Review, id=review_id)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        parent_id = request.POST.get('parent')
        
        if text:
            comment = ReviewComment.objects.create(
                review=review,
                author=request.user,
                text=text,
                parent_id=parent_id if parent_id else None
            )
            messages.success(request, 'Комментарий добавлен')
            
            if request.user != review.author:
                Notification.objects.create(
                    user=review.author,
                    notification_type='comment',
                    text=f'{request.user.username} прокомментировал ваш отзыв'
                )
        else:
            messages.error(request, 'Текст не может быть пустым')
    
    return redirect('car_detail', car_id=review.car.id)


@login_required
def like_review_comment(request, comment_id):
    """Лайк комментария к отзыву"""
    comment = get_object_or_404(ReviewComment, id=comment_id)
    
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        messages.info(request, 'Лайк убран')
    else:
        comment.likes.add(request.user)
        messages.success(request, 'Лайк поставлен')
    
    return redirect('car_detail', car_id=comment.review.car.id)
def compare_cars(request):
    """Сравнение нескольких автомобилей"""
    car_ids = request.GET.getlist('car_ids')
    
    # Очищаем список от пустых значений и преобразуем в числа
    car_ids = [int(cid) for cid in car_ids if cid and cid.strip()]
    
    # Убираем дубликаты и ограничиваем максимум 3
    car_ids = list(set(car_ids))[:3]
    
    cars = Car.objects.filter(id__in=car_ids) if car_ids else []
    all_cars = Car.objects.select_related('brand', 'model').all()
    
    # Считаем средний рейтинг для каждого автомобиля
    for car in cars:
        reviews = car.reviews.all()
        if reviews:
            car.avg_rating = sum(r.rating for r in reviews) / reviews.count()
        else:
            car.avg_rating = 0
    
    context = {
        'cars': cars,
        'all_cars': all_cars,
        'car_ids': car_ids,
    }
    return render(request, 'garage/compare_cars.html', context)
def search(request):
    """Поиск автомобилей по марке, модели или владельцу"""
    query = request.GET.get('q', '').strip()
    if query:
        cars = Car.objects.filter(
            models.Q(brand__name__icontains=query) |
            models.Q(model__name__icontains=query) |
            models.Q(owner__username__icontains=query)
        )
    else:
        cars = Car.objects.none()
    
    context = {
        'cars': cars,
        'query': query,
        'count': cars.count(),
    }
    return render(request, 'garage/search.html', context)