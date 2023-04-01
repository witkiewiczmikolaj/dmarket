from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<int:pk>/', views.user, name='user'),
    path('cart/<int:pk>/', views.cart, name='cart'),
]