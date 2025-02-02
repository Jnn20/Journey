from django.db import models
from user_module.models import User


class ArticleCategory(models.Model):
    title = models.CharField(max_length=100)
    # parent = models.ForeignKey('ArticleCategory', null=True, blank=True, on_delete=models.CASCADE)
    url_title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    reading_duration = models.IntegerField()
    image = models.ImageField(upload_to='articles_pic', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_author')
    short_description = models.CharField(max_length=100)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    slug = models.SlugField(null=True)
    categories = models.ManyToManyField(ArticleCategory)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ArticleComments(models.Model):
    # parent = models.ForeignKey('ArticleComments', on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    display = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} has left a comment for {self.article.title}'
