# Generated by Django 4.2.3 on 2023-09-07 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_place_district_place_location_place_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='photo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
