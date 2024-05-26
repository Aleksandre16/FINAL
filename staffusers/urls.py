from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import create_book, edit_book, delete_book

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('create_book/', create_book, name='create_book'),
    path('edit_book/<int:book_id>', edit_book, name='edit_book'),
    path('delete_book/<int:book_id>', delete_book, name='delete_book'),

]
