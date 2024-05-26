from urllib import request

from django.contrib.auth.models import AbstractUser
from django.db import models
from pyexpat.errors import messages

from FINAL import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    personal_number = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name', 'personal_number', 'date_of_birth']

    def __str__(self):
        return self.username


# models.py
class BorrowRecord(models.Model):
    book = models.ForeignKey('library.Book', on_delete=models.CASCADE, related_name='user_borrowrecord_set')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_borrowrecord_set')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)


class BorrowedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey('library.Book', on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
