# Generated by Django 5.1 on 2025-01-29 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0021_alter_articlecomments_article_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecomments',
            name='display',
            field=models.BooleanField(default=True),
        ),
    ]
