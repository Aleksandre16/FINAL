from django.urls import path
from . import views
from .views import *

app_name = 'library'

urlpatterns = [
    path('books/', views.BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    path('most-popular-books/', MostPopularBooks.as_view(), name='most_popular_books'),
    path('books-borrowed-last-year/', BooksBorrowedLastYear.as_view(), name='books_borrowed_last_year'), # 1
    path('books-returned-late/', BooksReturnedLate.as_view(), name='books_returned_late'), # 2
    path('top-late-users/', TopLateUsers.as_view(), name='top_late_users'), # 3
]
