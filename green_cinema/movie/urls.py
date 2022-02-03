from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main_view, name='main'),
    path('genre/', views.genre_view, name='genre'),
    path('contents/', views.contents_view, name='contents'),
]