from random import random
from django.core.management.base import BaseCommand
from faker import Faker
from library.models import Author, Genre, Book
import random

class Command(BaseCommand):
    help = 'Generate random books'

    def handle(self, *args, **kwargs):
        faker = Faker()
        genres = ['Fiction', 'Non-fiction', 'Science', 'History', 'Fantasy', 'Biography', 'Children', 'Romance']

        for genre in genres:
            Genre.objects.get_or_create(name=genre)

        for _ in range(100):
            Author.objects.create(name=faker.name())

        genre_objs = list(Genre.objects.all())
        author_objs = list(Author.objects.all())

        for _ in range(1000):
            title = faker.sentence(nb_words=4)
            pub_date = faker.date_between(start_date='-50y', end_date='today')
            quantity = random.randint(1, 20)
            genre = random.choice(genre_objs)
            book = Book.objects.create(title=title, genre=genre, pub_date=pub_date, quantity=quantity)
            author = random.choice(author_objs)
            book.authors.add(author)

        self.stdout.write(self.style.SUCCESS('Successfully generated books'))
