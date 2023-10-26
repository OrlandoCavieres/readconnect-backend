from django.db import models


class FinishedBook(models.Model):
    user = models.ForeignKey(to = 'Users.User', on_delete = models.CASCADE)
    book = models.ForeignKey(to = 'Books.Book', on_delete = models.CASCADE)

    added_on = models.DateTimeField(auto_now_add = True)
    removed_on = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return f'{self.id} | {self.user} -> {self.book}'


class WishReadBook(models.Model):
    user = models.ForeignKey(to = 'Users.User', on_delete = models.CASCADE)
    book = models.ForeignKey(to = 'Books.Book', on_delete = models.CASCADE)

    added_on = models.DateTimeField(auto_now_add = True)
    removed_on = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return f'{self.id} | {self.user} -> {self.book}'
