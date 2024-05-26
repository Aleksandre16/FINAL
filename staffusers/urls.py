from django.urls import path
from . import views
from .views import return_book, borrow_book

app_name = 'staffusers'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.staff_home, name='staff_home'),
    path('book/<int:pk>/borrow/', borrow_book, name='borrow-book'),
    path('book/<int:pk>/return/', return_book, name='return-book'),

]
