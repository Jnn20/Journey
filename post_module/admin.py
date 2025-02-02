from django.contrib import admin
from post_module.models import Post, PostComments


class PostCommentsInline(admin.TabularInline):
    model = PostComments
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish', 'user']
    inlines = [PostCommentsInline]
