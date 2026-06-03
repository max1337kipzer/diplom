from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/add_review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/like/', views.like_review, name='like_review'),
]