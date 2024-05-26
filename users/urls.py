from django.urls import path
from . import views
from .views import book_detail

app_name = 'users'

urlpatterns = [
    path('', views.users_home, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('book/<int:pk>/', book_detail, name='book-detail'),
]
