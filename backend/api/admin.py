from django.contrib import admin

from .models import (
    UserType,
    Campaign,
    CampaignImage,
    CampaignLogo,
    TargetDemographic,
    
    Topic,
    UserProfile,
    CityData,
    Location
)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city','phone_no')
    search_fields = ('user',)
    list_filter = ('user',)
    ordering = ('user',)

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type_pm')
    search_fields = ('user',)
    list_filter = ('user',)
    ordering = ('user',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('country', 'state', 'city', 'tier', 'population')
    search_fields = ('country',)
    list_filter = ('country',)
    ordering = ('country',)

admin.site.register(UserType,UserTypeAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Campaign)
admin.site.register(Location,LocationAdmin)
admin.site.register(CampaignImage)
admin.site.register(CampaignLogo)
admin.site.register(TargetDemographic)

admin.site.register(Topic)

@admin.register(CityData)
class CityDataAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'country', 'tier', 'city_population')
    search_fields = ('city', 'state', 'country', 'tier')
