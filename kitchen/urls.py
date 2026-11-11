from django.urls import path
from . import views


app_name = 'kitchen'

urlpatterns = [
    path('', views.idx_page, name='idx_kitchen'),
    path('tag/<slug:tag_slug>/', views.tag_list, name='post_list_by_tag'),
    path('<int:dish_id>/<slug:dish_slug>/comment/', views.dish_comment, name='dish_comment'),   
    path('<int:id>/<slug:slug>/', views.dish_detail, name='dish_detail'),
    path('list', views.dish_list, name='dish_list'),
    path('<slug:category_slug>/', views.dish_list, name='by_cat_list'),
]