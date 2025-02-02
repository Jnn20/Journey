from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff', 'phone']
    list_editable = ['is_active', 'is_staff']


admin.site.register(User, UserAdmin)

