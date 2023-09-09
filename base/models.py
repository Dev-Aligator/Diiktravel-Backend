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

# class Banner(models.Model):
#     tagLine = models.CharField(max_length=200, default="Welcome to my Portfolio")
#     plainText = models.CharField(max_length=500)
#     created = models.DateTimeField(auto_now_add=True)

# class Role(models.Model):
#     roleName = models.CharField(max_length=200)
#     created = models.DateTimeField(auto_now_add=True)
#     banner = models.ForeignKey(Banner, on_delete=models.CASCADE, related_name="roles")

#     def __str__(self):
#         return self.roleName

# class Skill(models.Model):
#     skillPercentage = models.PositiveSmallIntegerField(default=90)
#     stopColor1 = models.CharField(max_length=20, null=True, blank=True)
#     stopColor2 = models.CharField(max_length=20, null=True, blank=True)    
#     skillName = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.skillName

# class Project(models.Model):
#     title = models.CharField(max_length=200, unique=True)
#     description = models.CharField(max_length=200)
#     imgUrl = models.ImageField(upload_to="images/")
#     tabIndex = models.PositiveSmallIntegerField(default=1)
    
#     def __str__(self):
#         return self.title

# class Contact(models.Model):
#     firstName = models.CharField(max_length=200)
#     lastName = models.CharField(max_length=200)
#     email = models.EmailField(max_length=50)
#     phone = models.CharField(max_length=20, null=True, blank=True)
#     message = models.CharField(max_length=500)
#     created = modles.DateTimeField(auto_now_add=true)

#     def ___str__(self):
#         return self.firstName + self.lastName

    

