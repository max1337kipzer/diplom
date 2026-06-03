from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/add_review/', views.add_review, name='add_review'),
    path('search/', views.search, name='search'),
    path('add_car/', views.add_car, name='add_car'),
    path('get_models/', views.get_models, name='get_models'),
    path('review/<int:review_id>/comment/add/', views.add_review_comment, name='add_review_comment'),
    path('review_comment/<int:comment_id>/like/', views.like_review_comment, name='like_review_comment'),
]