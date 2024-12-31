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
    Topic,
    UserProfile
)


class UserProfileAdmin(admin.ModelAdmin):
    # Display the following fields in the list view
    list_display = ('user', 'city','phone_no')

    # Add search functionality
    search_fields = ('user',)

    # Add filtering options
    list_filter = ('user',)

    # Optionally, add ordering to the list view
    ordering = ('user',)

class UserTypeAdmin(admin.ModelAdmin):
    # Display the following fields in the list view
    list_display = ('user', 'user_type_pm')

    # Add search functionality
    search_fields = ('user',)

    # Add filtering options
    list_filter = ('user',)

    # Optionally, add ordering to the list view
    ordering = ('user',)
admin.site.register(UserType,UserTypeAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Campaign)
admin.site.register(CampaignImage)
admin.site.register(CampaignLogo)
admin.site.register(TargetDemographic)
admin.site.register(Keyword)
admin.site.register(Topic)
