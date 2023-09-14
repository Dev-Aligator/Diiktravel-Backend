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