from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type_pm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="campaigns",blank=True, null=True)
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
    file = models.FileField(upload_to='campaigns/',null=True, blank=True)
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
