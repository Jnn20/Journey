# Generated by Django 5.1 on 2024-09-03 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0004_article_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url_title', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='article_module.articlecategory'),
        ),
    ]
