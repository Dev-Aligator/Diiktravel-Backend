# Generated by Django 4.2.3 on 2023-09-11 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_place_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='distance_to_user',
            field=models.FloatField(blank=True, null=True),
        ),
    ]