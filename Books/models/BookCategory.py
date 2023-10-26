from django.db import models


class BookCategory(models.Model):
    name = models.CharField(max_length = 80)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Book Categories'
