# Generated by Django 5.1.2 on 2024-12-15 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_api', '0003_savedarticle_delete_note'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SavedArticle',
        ),
    ]
