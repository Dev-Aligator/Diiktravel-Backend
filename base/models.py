from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.



class Place(models.Model):
    googleMapId = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    types = models.CharField(max_length=500, default="")
    location = models.CharField(max_length=50, default="")
    district = models.CharField(max_length=50, default="")
    rating = models.FloatField(null=True,blank=True)
    totalRating = models.FloatField(null=True,blank=True)
    photo = models.CharField(max_length=200, null=True, blank=True)

    distance_to_user = models.FloatField(null=True, blank=True)


class PlaceDetails(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    current_opening_hours = models.CharField(max_length=255, blank=True, null=True)
    formatted_phone_number = models.CharField(max_length=20, blank=True, null=True)
    international_phone_number = models.CharField(max_length=20, blank=True, null=True)
    opening_hours = models.CharField(max_length=255, blank=True, null=True)
    secondary_opening_hours = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    curbside_pickup = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    dine_in = models.BooleanField(default=False)
    editorial_summary = models.TextField(blank=True, null=True)
    price_level = models.PositiveIntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    reservable = models.BooleanField(default=False)
    serves_beer = models.BooleanField(default=False)
    serves_breakfast = models.BooleanField(default=False)
    serves_dinner = models.BooleanField(default=False)
    serves_lunch = models.BooleanField(default=False)
    serves_vegetarian_food = models.BooleanField(default=False)
    serves_wine = models.BooleanField(default=False)
    takeout = models.BooleanField(default=False)
    user_ratings_total = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.id


class UserFeature(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=20, null=True, blank=True)
    lastName = models.CharField(max_length=20, null=True, blank=True)
    lastLatitude = models.FloatField(null=True, blank=True)
    lastLongitude = models.FloatField(null=True, blank=True)
    # Add other fields for user details like oldest location, interests, etc.

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_feature(sender, instance, created, **kwargs):
    if created:
        UserFeature.objects.create(user=instance)

# Connect the signal
post_save.connect(create_user_feature, sender=User)