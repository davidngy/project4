# Generated by Django 4.2.7 on 2024-01-06 15:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='liked',
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
