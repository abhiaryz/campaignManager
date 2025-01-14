from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import re

class Location(models.Model):
    country = models.CharField(max_length=254)
    state = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    tier = models.CharField(max_length=254)
    population = models.CharField(max_length=254)


class CityData(models.Model):
    TIER_CHOICES = [
        ('Tier-I', 'Tier-I'),
        ('Tier-II', 'Tier-II'),
    ]

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES)
    city_population = models.BigIntegerField()

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"

class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type_pm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="campaigns",blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    age = models.JSONField(blank=True, null=True)
    day_part = models.CharField(max_length=255, blank=True, null=True)
    device = models.JSONField(blank=True, null=True)
    environment = models.JSONField(blank=True, null=True)

    exchange = models.JSONField(blank=True, null=True)
    interset = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    language = models.JSONField(blank=True, null=True)
    carrier = models.JSONField(blank=True, null=True)
    device_price = models.JSONField(blank=True, null=True)
    
    start_time = models.CharField(max_length=5, blank=True, null=True)
    end_time = models.CharField(max_length=5, blank=True, null=True)

    proximity_store = models.ManyToManyField(
        'proximity_store',
        blank=True,
        related_name='proximity_store',
    )

    proximity = models.ManyToManyField(
        'proximity',
        blank=True,
        related_name='proximity',
    )

    weather = models.ManyToManyField(
        'weather',
        blank=True,
        related_name='weather',
    )

    location = models.ManyToManyField(
        'location',
        blank=True,
        related_name='Location',
    )

    images = models.ManyToManyField(
        'CampaignImage',
        blank=True,
        related_name='campaign_images',
    )
    logos = models.ManyToManyField(
        'CampaignLogo',
        blank=True,
        related_name='campaign_logos',
    )
    video = models.FileField(
        upload_to='campaigns/videos/',
        null=True,
        blank=True,
    )

    keywords = models.ManyToManyField(
        'Keyword',
        blank=True,
        related_name='campaign_keywords',
    )


    def clean(self):
        super().clean()
        # Validate start_time and end_time format (HH:MM)
        time_pattern = r'^\d{2}:\d{2}$'
        if self.start_time and not re.match(time_pattern, self.start_time):
            raise ValidationError({'start_time': 'Invalid time format. Should be HH:MM.'})
        if self.end_time and not re.match(time_pattern, self.end_time):
            raise ValidationError({'end_time': 'Invalid time format. Should be HH:MM.'})

class CampaignImage(models.Model):
    image = models.ImageField(upload_to='campaigns/images/')
    created_at = models.DateTimeField(auto_now_add=True)

class CampaignLogo(models.Model):
    logo = models.ImageField(upload_to='campaigns/logos/')
    created_at = models.DateTimeField(auto_now_add=True)

class TargetDemographic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
from datetime import datetime
class Keyword(models.Model):
    file = models.FileField(upload_to='campaign_keywords/',blank=True,null=True)
    uploaded_at = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return f"File {self.id} uploaded at {self.uploaded_at}"

class proximity_store(models.Model):
    file = models.FileField(upload_to='proximity_store/',blank=True,null=True)
    uploaded_at = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return f"File {self.id} uploaded at {self.uploaded_at}"

class proximity(models.Model):
    file = models.FileField(upload_to='proximity/',blank=True,null=True)
    uploaded_at = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return f"File {self.id} uploaded at {self.uploaded_at}"

class weather(models.Model):
    file = models.FileField(upload_to='weather/',blank=True,null=True)
    uploaded_at = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return f"File {self.id} uploaded at {self.uploaded_at}"
            
class Topic(models.Model):
    topic = models.CharField(max_length=100)

    def __str__(self):
        return self.topic
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    city = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
