from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('authors', views.AuthorViewSet)
router.register('genres', views.GenreViewSet)
router.register('books', views.BookViewSet)
router.register('borrow_records', views.BorrowRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
