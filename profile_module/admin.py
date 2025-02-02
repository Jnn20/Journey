from django.contrib import admin
from profile_module.models import Profile
from user_module.models import Contact


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contact)
