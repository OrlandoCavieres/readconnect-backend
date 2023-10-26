from django.contrib import admin

from Interactions.models import BookReview


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book']
