from django.contrib import admin
from .models import Article, ArticleCategory, ArticleComments


class ArticleCommentsInline(admin.TabularInline):
    model = ArticleComments
    fields = ['parent', 'display', 'user', 'text', 'created']
    ordering = ['-created']
    readonly_fields = ['created']
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_active']
    list_editable = ['is_active']
    inlines = [ArticleCommentsInline]


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = ['is_active']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
