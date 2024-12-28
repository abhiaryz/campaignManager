from django.db import models

class Campaign(models.Model):
    CAMPAIGN_TYPE_CHOICES = [
        ('image', 'Image Campaign'),
        ('video', 'Video Campaign'),
    ]

    name = models.CharField(max_length=255)
    campaign_type = models.CharField(max_length=10, choices=CAMPAIGN_TYPE_CHOICES)
    text = models.TextField(null=True, blank=True)  # For image campaigns
    geo_location = models.CharField(max_length=255, null=True, blank=True)  # For image campaigns
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # For image campaigns
    file = models.FileField(upload_to='campaigns/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
