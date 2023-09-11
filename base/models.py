from django.db import models
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

