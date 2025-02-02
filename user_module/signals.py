from django.db.models.signals import post_save
from django.dispatch import receiver
from profile_module.models import Profile
from user_module.models import User


@receiver(post_save, sender=User)
def fill_profile(sender, instance: User, created, **kwargs):
    if instance.is_active and not Profile.objects.filter(user=instance):
        new_profile = Profile.objects.create(user=instance)
        new_profile.telegram = 'not set yet'
        new_profile.instagram = 'not set yet'
        new_profile.linkedin = 'not set yet'
        new_profile.job = 'not set yet'
        new_profile.about = 'hi I am a newcomer and I will write about myself here asap.'
        new_profile.save()
