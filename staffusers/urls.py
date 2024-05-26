from django.urls import path
from . import views

app_name = 'staffusers'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.staff_home, name='staff_home'),  # Keep only one definition of staff_home
    path('add/', views.add_book, name='add_book'),
    path('<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('<int:book_id>/edit/', views.edit_book, name='edit_book'),
]
