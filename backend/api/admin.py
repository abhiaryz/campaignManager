from django.contrib import admin

from .models import (
    Campaign,
    CampaignImage,
    CityData,
    Keyword,
    Location,
    UserProfile,
    UserType,
    target_type,
    Age,
    CarrierData,
    Environment,
    Exchange,
    Language,
    Impression,
    DevicePrice,
    Device,
    DistinctInterest,
)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "phone_no")
    search_fields = ("user",)
    list_filter = ("user",)
    ordering = ("user",)


class UserTypeAdmin(admin.ModelAdmin):
    list_display = ("user", "user_type_pm")
    search_fields = ("user",)
    list_filter = ("user",)
    ordering = ("user",)


class LocationAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "city", "tier", "population")
    search_fields = ("country",)
    list_filter = ("country",)
    ordering = ("country",)


admin.site.register(UserType, UserTypeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Campaign)
admin.site.register(Location, LocationAdmin)
admin.site.register(target_type)
admin.site.register(CampaignImage)
admin.site.register(Keyword)
admin.site.register(Age)
admin.site.register(CarrierData)
admin.site.register(Environment)
admin.site.register(Exchange)
admin.site.register(Language)
admin.site.register(Impression)
admin.site.register(DevicePrice)
admin.site.register(Device)
admin.site.register(DistinctInterest)


@admin.register(CityData)
class CityDataAdmin(admin.ModelAdmin):
    list_display = ("city", "state", "country", "tier", "city_population")
    search_fields = ("city", "state", "country", "tier")
