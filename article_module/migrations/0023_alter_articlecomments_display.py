# Generated by Django 5.1 on 2025-01-29 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0022_alter_articlecomments_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecomments',
            name='display',
            field=models.BooleanField(default=False),
        ),
    ]
