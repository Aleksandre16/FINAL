from django.db import models

from FINAL import settings


class Author(models.Model):
    name = models.CharField(max_length=100)


class Genre(models.Model):
    name = models.CharField(max_length=200)


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    pub_date = models.DateField('Publication date')
    quantity = models.IntegerField(default=1)


class BorrowRecord(models.Model):
    book = models.ForeignKey('library.Book', on_delete=models.CASCADE, related_name='lib_borrowrecord_set')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lib_borrowrecord_set')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

