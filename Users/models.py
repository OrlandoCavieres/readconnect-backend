from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length = 100, null = True, blank = True)
    email = models.EmailField(unique = True)

    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    books_finished = models.ManyToManyField(to = 'Books.Book', through = 'Books.FinishedBook',
                                            blank = True, related_name = 'users_finished')
    books_wish_list = models.ManyToManyField(to = 'Books.Book', through = 'Books.WishReadBook',
                                             blank = True, related_name = 'users_wish_list')

    book_reviews = models.ManyToManyField(to = 'Books.Book', through = 'Interactions.BookReview',
                                          blank = True, related_name = 'user_reviews')

    def __str__(self):
        return f'{self.email}'
