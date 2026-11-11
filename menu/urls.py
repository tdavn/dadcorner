from django.urls import path
from . import views


app_name = 'menu'

urlpatterns = [
    path('', views.menu_detail, name='menu_detail'),
    path('add/<int:dish_id>/', views.menu_add, name='menu_add'),
    path('remove/<int:dish_id>/', views.menu_remove, name='menu_remove'),
]