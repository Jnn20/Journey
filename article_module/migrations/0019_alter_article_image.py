# Generated by Django 5.1 on 2025-01-27 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0018_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='articles_pic'),
        ),
    ]
