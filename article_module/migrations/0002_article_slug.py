# Generated by Django 5.1 on 2024-08-21 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
