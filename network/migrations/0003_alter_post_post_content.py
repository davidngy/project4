# Generated by Django 4.2.7 on 2024-01-01 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_alter_post_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
