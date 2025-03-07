# Generated by Django 5.1 on 2025-01-18 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_module', '0001_initial'),
        ('article_module', '0016_remove_article_saved_by_users_delete_savedarticles'),
        ('post_module', '0008_post_likes_delete_postlikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='activity_score',
            field=models.PositiveIntegerField(default=0, verbose_name='activity score'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='liked_posts',
            field=models.ManyToManyField(related_name='liked_by', to='post_module.post'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='saved_articles',
            field=models.ManyToManyField(related_name='saved_by', to='article_module.article'),
        ),
    ]
