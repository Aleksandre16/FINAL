from datetime import timezone
from library.serializers import BookSerializer, BorrowRecordSerializer, UserSerializer
from django.db.models import Count, F, Q
from library.models import Book
from users.models import User, BorrowRecord
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class MostPopularBooks(generics.ListAPIView):
    queryset = Book.objects.annotate(num_borrowed=Count('borrow_records')).order_by('-num_borrowed')[:10]
    serializer_class = BookSerializer


class BooksBorrowedLastYear(generics.ListAPIView):
    queryset = BorrowRecord.objects.filter(borrowed_at__year=timezone.now().year - 1).select_related('book').values(
        'book__title').annotate(total_borrowed=Count('book__title'))
    serializer_class = BorrowRecordSerializer


class BooksReturnedLate(generics.ListAPIView):
    queryset = BorrowRecord.objects.filter(
        returned_at__gt=F('borrowed_at') + timezone.timedelta(days=30)).select_related('book').values(
        'book__title').annotate(times_late=Count('book__title'))
    serializer_class = BorrowRecordSerializer


class TopLateUsers(generics.ListAPIView):
    queryset = User.objects.annotate(num_late=Count('borrow_records__returned_at__gt', filter=Q(
        borrow_records__returned_at__gt=F('borrow_records__borrowed_at') + timezone.timedelta(days=30)))).order_by(
        '-num_late')[:100]
    serializer_class = UserSerializer
