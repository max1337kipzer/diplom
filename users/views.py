from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from garage.models import Car, Review

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request, username=None):
    if username:
        user = User.objects.get(username=username)
    else:
        user = request.user
    
    cars = Car.objects.filter(owner=user)
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