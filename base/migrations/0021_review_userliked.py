# Generated by Django 4.2.3 on 2023-09-18 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_review_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='userLiked',
            field=models.TextField(default=''),
        ),
    ]