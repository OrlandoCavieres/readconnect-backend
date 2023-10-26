from django.contrib import admin

from Users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ['is_superuser']
    list_display = ['id', 'email', 'is_staff', 'is_superuser']
    search_fields = ['email']
