import re
from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Location(models.Model):
    country = models.CharField(max_length=254)
    state = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    tier = models.CharField(max_length=254)
    population = models.CharField(max_length=254)

class DevicePrice(models.Model):
    price = models.CharField(max_length=254, unique=True)

class Device(models.Model):
    device = models.CharField(max_length=254, unique=True)

class DistinctInterest(models.Model):
    interest = models.CharField(max_length=254, unique=True)

class Age(models.Model):
    age = models.CharField(max_length=254)

class CarrierData(models.Model):
    carrier = models.CharField(max_length=254)

class Environment(models.Model):
    env = models.CharField(max_length=254)

class Exchange(models.Model):
    exchange = models.CharField(max_length=254)

class Language(models.Model):
    language = models.CharField(max_length=254)
    iso_code = models.CharField(max_length=254, blank=True, null=True,default="")

class Impression(models.Model):
    impression = models.JSONField()

class CityData(models.Model):
    TIER_CHOICES = [
        ("Tier-I", "Tier-I"),
        ("Tier-II", "Tier-II"),
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
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="campaigns", blank=True, null=True
    )
    objective = models.CharField(max_length=50, choices=[('Banner', 'BANNER'), ('Video', 'VIDEO')], blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    age = models.JSONField(blank=True, null=True)
    day_part = models.CharField(max_length=255, blank=True, null=True)
    device = models.JSONField(blank=True, null=True)
    environment = models.JSONField(blank=True, null=True)

    exchange = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    language = models.JSONField(blank=True, null=True)
    carrier = models.JSONField(blank=True, null=True)
    device_price = models.JSONField(blank=True, null=True)

    total_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    landing_page = models.CharField(max_length=256, blank=True, null=True)
    reports_url = models.URLField(max_length=256, blank=True, null=True)
    tag_tracker = models.CharField(max_length=255, blank=True, null=True)

    start_time = models.CharField(max_length=256, blank=True, null=True)
    end_time = models.CharField(max_length=256, blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Created', 'CREATED'),
            ('Learning', 'LEARNING'),
            ('Live', 'LIVE'),
            ('Pause Option', 'PAUSE OPTION'),
            ('Completed', 'COMPLETED'),
            ('Other', 'Other')
        ],
        blank=True,
        null=True,
        default='Created'  # Set the default here
    )

    viewability = models.PositiveIntegerField(default=0)
    brand_safety = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    ctr = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    views = models.PositiveIntegerField(default=0)
    vtr = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    buy_type = models.CharField(max_length=50, choices=[('CPM', 'CPM'), ('CVC', 'CVC'), ('Other', 'Other')], blank=True, null=True)
    unit_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    proximity_store = models.ManyToManyField(
        "proximity_store",
        blank=True,
        related_name="proximity_store",
    )

    proximity = models.ManyToManyField(
        "proximity",
        blank=True,
        related_name="proximity",
    )

    weather = models.ManyToManyField(
        "weather",
        blank=True,
        related_name="weather",
    )

    location = models.ManyToManyField(
        "location",
        blank=True,
        related_name="Location",
    )

    target_type = models.ManyToManyField(
        "target_type",
        blank=True,
        related_name="target_type",
    )

    images = models.ManyToManyField(
        "CampaignImage",
        blank=True,
        related_name="campaign_images",
    )
    video = models.ManyToManyField(
        "CampaignVideo",
        blank=True,
        related_name ="Campaign_video",
    )
    keywords = models.ManyToManyField(
        "Keyword",
        blank=True,
        related_name="campaign_keywords",
    )



class CampaignImage(models.Model):
    image = models.FileField(upload_to="campaigns/images/")
    created_at = models.DateTimeField(auto_now_add=True)

class CampaignVideo(models.Model):
    video = models.FileField(upload_to="campaigns/video/")
    created_at = models.DateTimeField(auto_now_add=True)

class Keyword(models.Model):
    file = models.FileField(upload_to="campaign_keywords/", blank=True, null=True)
    uploaded_at = models.DateTimeField(default=datetime.now, blank=True)
    keywords = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"File {self.id} uploaded at {self.uploaded_at}"


class proximity_store(models.Model):
    file = models.FileField(upload_to="proximity_store/", blank=True, null=True)
    uploaded_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"File {self.id} uploaded at {self.uploaded_at}"

class Bidding_detail(models.Model):
    buy_type = models.CharField(max_length=50, choices=[('CPM', 'CPM'), ('CVC', 'CVC'), ('Other', 'Other')], blank=True, null=True)
    unit_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f"File {self.id} uploaded at {self.buy_type}"

class proximity(models.Model):
    file = models.FileField(upload_to="proximity/", blank=True, null=True)
    uploaded_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"File {self.id} uploaded at {self.uploaded_at}"


class weather(models.Model):
    file = models.FileField(upload_to="weather/", blank=True, null=True)
    uploaded_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"File {self.id} uploaded at {self.uploaded_at}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    city = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)


class target_type(models.Model):
    targeting_type = models.CharField(max_length=255)
    category = models.CharField(max_length=255, default='', blank=True, null=True)
    subcategory = models.CharField(max_length=255, blank=True, null=True, default='')


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
