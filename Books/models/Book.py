from datetime import datetime

from django.db import models

from Users.models import User


class Book(models.Model):
    title = models.CharField(max_length = 100)
    isbn = models.CharField(max_length = 50)
    page_count = models.PositiveIntegerField(default = 0)

    authors = models.ManyToManyField(to = 'Books.Author', blank = True, related_name = 'books')
    categories = models.ManyToManyField(to = 'Books.BookCategory', blank = True, related_name = 'books')

    thumbnail = models.URLField()

    short_description = models.CharField(max_length = 200)
    long_description = models.TextField()

    status = models.CharField(max_length = 15)
    published_date = models.DateTimeField(null = True, blank = True)

    @property
    def authors_str_ordered(self) -> str:
        return ', '.join([author.name for author in self.authors.all().order_by('name')])

    @property
    def categories_str_ordered(self) -> str:
        return ', '.join([category.name for category in self.categories.all().order_by('name')])

    @property
    def rating(self) -> float:
        if self.reviews_number == 0:
            return -1

        suma_total = sum([review.rating for review in self.reviews.all()])
        return suma_total / self.reviews_number

    @property
    def reviews_number(self) -> int:
        return self.reviews.all().count()

    @property
    def published_date_format(self) -> str:
        return datetime.strftime(self.published_date, "%d/%m/%Y") if self.published_date else 'Desconocida'

    def in_user_wished_list(self, user: User) -> bool:
        return user.books_wish_list.filter(id = self.id).exists()

    def in_user_finished_list(self, user: User) -> bool:
        return user.books_finished.filter(id = self.id).exists()

    def __str__(self):
        return self.title
