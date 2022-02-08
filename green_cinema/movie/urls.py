from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('main/', views.main_view, name='main'),
    path('genre/', views.genre_view, name='genre'),
    path('contents/<int:id>', views.contents_view, name='contents'),
    path('contents/api/rating_create/<int:id>', views.rating_create, name='rating_create'),
    path('contents/api/rating_update/<int:id>', views.rating_update, name='rating_update'),
]