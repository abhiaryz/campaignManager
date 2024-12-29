from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    UserType,
    Campaign,
    CampaignImage,
    CampaignLogo,
    TargetDemographic,
    Keyword,
    Topic
)
admin.site.register(UserType)
admin.site.register(Campaign)
admin.site.register(CampaignImage)
admin.site.register(CampaignLogo)
admin.site.register(TargetDemographic)
admin.site.register(Keyword)
admin.site.register(Topic)
