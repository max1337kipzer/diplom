from django.shortcuts import render
from .models import Car

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'garage/car_list.html', {'cars': cars})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Car, Review

def car_detail(request, car_id):
    """Детальная страница автомобиля"""
    car = get_object_or_404(Car, id=car_id)
    reviews = car.reviews.all()
    
    # Средняя оценка
    if reviews.exists():
        avg_rating = sum(r.rating for r in reviews) / reviews.count()
    else:
        avg_rating = 0
    
    # Проверял ли пользователь уже лайкнул отзыв (пока не используем)
    
    context = {
        'car': car,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'reviews_count': reviews.count(),
    }
    return render(request, 'garage/car_detail.html', context)


@login_required
def add_review(request, car_id):
    """Добавление отзыва об автомобиле"""
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
            messages.success(request, 'Отзыв успешно добавлен!')
        else:
            messages.error(request, 'Заполните все поля')
        
        return redirect('car_detail', car_id=car.id)
    
    return redirect('car_detail', car_id=car.id)


@login_required
def like_review(request, review_id):
    """Лайк отзыва"""
    review = get_object_or_404(Review, id=review_id)
    
    if request.user in review.likes.all():
        review.likes.remove(request.user)
        messages.info(request, 'Вы убрали лайк')
    else:
        review.likes.add(request.user)
        messages.success(request, 'Вы поставили лайк')
    
    return redirect('car_detail', car_id=review.car.id)