from django.db import models
from django.contrib.auth.models import User

class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type_pm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Campaign(models.Model):
    CAMPAIGN_TYPE_CHOICES = [
        ('image', 'Image Campaign'),
        ('video', 'Video Campaign'),
    ]
    final_url = models.CharField(max_length=255,blank=True, null=True)
    business_name = models.CharField(max_length=255,blank=True, null=True)
    campaign_type = models.CharField(max_length=10, choices=CAMPAIGN_TYPE_CHOICES)
    text = models.TextField(null=True, blank=True)
    geo_location = models.CharField(max_length=255, null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    file = models.FileField(upload_to='campaigns/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(max_length=255,blank=True, null=True)
    bidding = models.CharField(max_length=255,blank=True, null=True)
    bidding_focus = models.CharField(max_length=255,blank=True, null=True)
    target_people = models.CharField(max_length=255,blank=True, null=True)
    target_content = models.CharField(max_length=255,blank=True, null=True)
    target_optimize = models.BooleanField(default=True)
    
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
    target_demographics = models.ManyToManyField(
        'TargetDemographic',
        blank=True,
        related_name='campaign_demographics',
    )
    keywords = models.ManyToManyField(
        'Keyword',
        blank=True,
        related_name='campaign_keywords',
    )
    topics = models.ManyToManyField(
        'Topic',
        blank=True,
        related_name='campaign_topics',
    )


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


class Keyword(models.Model):
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.keyword


class Topic(models.Model):
    topic = models.CharField(max_length=100)

    def __str__(self):
        return self.topic