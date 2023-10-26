from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from Users.models import User


class BookReview(models.Model):
    user = models.ForeignKey(to = 'Users.User', null = True, blank = True, on_delete = models.SET_NULL, related_name = 'reviews')
    book = models.ForeignKey(to = 'Books.Book', null = True, blank = True, on_delete = models.SET_NULL, related_name = 'reviews')

    body = models.TextField()
    rating = models.PositiveIntegerField(validators = [MinValueValidator(1), MaxValueValidator(5)])

    created_at = models.DateTimeField(auto_now_add = True)
    last_update = models.DateTimeField(auto_now = True)

    @property
    def last_update_format(self) -> str:
        return self.last_update.strftime('%H:%M - %d/%m/%Y')

    def created_by_logged_user(self, user: User) -> bool:
        return user.reviews.filter(id = self.id).exists()

    def __str__(self):
        return f'{self.id} | {self.book} - {self.user}'
