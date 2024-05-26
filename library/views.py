from rest_framework import viewsets
from .models import Author, Genre, Book, BorrowRecord
from .serializers import AuthorSerializer, GenreSerializer, BookSerializer, BorrowRecordSerializer
from django.shortcuts import render


def index(request):
    return render(request, 'library/index.html')


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer


