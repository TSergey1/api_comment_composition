from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# @admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
        'bio'
    )
    list_editable = (
        'email',
        'role',
        'first_name',
        'last_name',
        'bio'
    )
    search_fields = ('username',)
    list_filter = ('username',)


admin.site.register(User, UserAdmin)
