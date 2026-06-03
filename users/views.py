from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from garage.models import Car, Review

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request, username=None):
    """Личный кабинет пользователя"""
    if username:
        user = User.objects.get(username=username)
    else:
        user = request.user
    
    # Получаем автомобили пользователя
    cars = Car.objects.filter(owner=user)
    
    # Получаем отзывы пользователя
    reviews = Review.objects.filter(author=user)
    
    context = {
        'profile_user': user,
        'cars': cars,
        'reviews': reviews,
        'cars_count': cars.count(),
        'reviews_count': reviews.count(),
        'is_own_profile': request.user == user,
    }
    return render(request, 'users/profile.html', context)