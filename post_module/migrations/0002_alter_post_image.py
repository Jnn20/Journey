# Generated by Django 5.1 on 2024-10-26 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/posts/'),
        ),
    ]
