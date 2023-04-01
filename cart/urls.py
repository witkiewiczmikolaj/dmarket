from django.urls import path
from . import views

app_name= 'cart'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/<int:pk>', views.add_item, name='add'),
    path('remove/<int:pk>', views.remove_item, name='remove'),
]