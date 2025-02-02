from django.db.models.signals import post_save
from django.dispatch import receiver
from profile_module.models import Profile
from article_module.models import ArticleComments
from post_module.models import Post, PostComments


@receiver(post_save, sender=Post)
def post_create_score(instance, created, sender, **kwargs):
    if created:
        profile = Profile.objects.get(user_id=instance.user.id)
        profile.activity_score += 5
        profile.save()


@receiver(post_save, sender=PostComments)
def post_comment_score(instance, created, sender, **kwargs):
    if created:
        profile = Profile.objects.get(user_id=instance.user.id)
        profile.activity_score += 1
        profile.save()


@receiver(post_save, sender=ArticleComments)
def article_comment_score(instance, created, sender, **kwargs):
    if created:
        profile = Profile.objects.get(user_id=instance.user.id)
        profile.activity_score += 3
        profile.save()

