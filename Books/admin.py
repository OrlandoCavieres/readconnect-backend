from django.contrib import admin

from Books.models import Author, BookCategory, Book, WishReadBook, FinishedBook


@admin.register(Author, BookCategory)
class AuthorBookCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']
    list_filter = ['status']


@admin.register(FinishedBook, WishReadBook)
class BookListsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book']
    search_fields = ['user', 'book']
