from django.contrib import admin
from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_authors', 'display_genre']

    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])

    display_authors.short_description = 'Authors'

    def display_genre(self, obj):
        return obj.genre.name

    display_genre.short_description = 'Genre'

    search_fields = ['title', 'authors__name', 'genre__name']
