# Generated by Django 5.1 on 2024-11-02 17:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_module', '0006_postlikes_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='like', through='post_module.PostLikes', to=settings.AUTH_USER_MODEL),
        ),
    ]
