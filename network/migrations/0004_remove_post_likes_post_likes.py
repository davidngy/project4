# Generated by Django 4.2.7 on 2024-01-02 22:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_post_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]