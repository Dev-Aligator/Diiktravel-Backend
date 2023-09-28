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

class Review(models.Model):
    author_id = models.CharField(blank=True, null=True, max_length=50)
    place_id = models.CharField(blank=True, null=True, max_length=50)
    author_name = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    relative_time_description = models.CharField(max_length=255, null=True, blank=True)
    time = models.BigIntegerField()
    language = models.CharField(max_length=10, blank=True, null=True)
    original_language = models.CharField(max_length=10, blank=True, null=True)
    profile_photo_url = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    translated = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(default=0)
    userLiked = models.TextField(max_length=None, default="")
    
    def __str__(self):
        return f'Review by {self.author_name} - Rating: {self.rating}'


class UserSavePlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)  # Link to the Place model
    saved_date = models.DateTimeField(auto_now_add=True)  # This sets the date to auto add when an instance is created

    class Meta:
        unique_together = ['user', 'place']

    def __str__(self):
        return f"SavedPlace by {self.user} - Place ID: {self.place_id}"

class UserLeftReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'review']

    def __str__(self):
        return f"Review by {self.user} - ID: {self.review.id}"
class UserFeature(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=20, null=True, blank=True)
    lastName = models.CharField(max_length=20, null=True, blank=True)
    lastLatitude = models.FloatField(null=True, blank=True)
    lastLongitude = models.FloatField(null=True, blank=True)
    photoUrl = models.URLField(null=True, blank=True)
    # Add other fields for user details like oldest location, interests, etc.

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_feature(sender, instance, created, **kwargs):
    if created:
        UserFeature.objects.create(user=instance)

# Connect the signal
post_save.connect(create_user_feature, sender=User)

