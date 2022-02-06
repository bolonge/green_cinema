from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/', views.logout, name='logout'),
    # path('user/', views.user_view, name='user'), ## 굳이 이 url이 필요한가 싶은...
    path('user/<int:id>/', views.user_view, name='user'),
] 