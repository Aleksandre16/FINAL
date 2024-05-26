from django.urls import path
from . import views
from .views import BookDetailView, borrow_book, cancel_reservation

app_name = 'users'

urlpatterns = [
    path('', views.users_home, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/borrow/', borrow_book, name='borrow-book'),
    path('cancel/<int:pk>/', cancel_reservation, name='cancel-reservation')

]
