# Generated by Django 5.1 on 2024-09-06 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0006_articlecategory_parent_alter_article_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlecategory',
            name='parent',
        ),
    ]
