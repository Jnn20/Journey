from django.db import models
from article_module.models import Article
from post_module.models import Post
from user_module.models import User


class Profile(models.Model):
    # info
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile', blank=False, verbose_name='user')
    avatar = models.ImageField(upload_to='avatars', verbose_name='profile picture', null=True, blank=True)
    telegram = models.CharField(max_length=50, verbose_name='telegram link', null=True, blank=True)
    instagram = models.CharField(max_length=50, verbose_name='instagram link', null=True, blank=True)
    linkedin = models.CharField(max_length=50, verbose_name='linked-in link', null=True, blank=True)
    job = models.CharField(max_length=50, verbose_name='your job', null=True, blank=True)
    about = models.TextField(verbose_name='about you', null=True, blank=True)
    # activities
    activity_score = models.PositiveIntegerField(verbose_name='activity score', default=0)
    saved_articles = models.ManyToManyField(Article, related_name='saved_by')
    liked_posts = models.ManyToManyField(Post, related_name='liked_by')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

