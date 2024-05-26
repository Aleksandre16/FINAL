from django.contrib import admin
from django.contrib import admin

from users.models import BorrowRecord, BorrowedBook
from .models import Book, Author, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_authors', 'display_genre']

    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])

    display_authors.short_description = 'Authors'

    def display_genre(self, obj):
        return obj.genre.name

    display_genre.short_description = 'Genre'

    search_fields = ['title', 'authors__name', 'genre__name']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(BorrowRecord)
admin.site.register(BorrowedBook)
