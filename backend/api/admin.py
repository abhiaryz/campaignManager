from django.contrib import admin

from .models import (
    Campaign,
    CampaignImage,
    CampaignVideo,
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
    BrandSafety,
    BuyType,
    Bidding_detail,
    Viewability
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


class LanguageAdmin(admin.ModelAdmin):
    list_display = ("language", "iso_code", "label")
    search_fields = ("language",)
    list_filter = ("language",)
    ordering = ("language",)

class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("exchange", "label")
    search_fields = ("exchange",)
    list_filter = ("exchange",)
    ordering = ("exchange",)

class CarrierDataAdmin(admin.ModelAdmin):
    list_display = ("carrier", "label")

class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ("env", "label")


class BrandSafetyAdmin(admin.ModelAdmin):
    list_display = ("value", "label")

class BuyTypeAdmin(admin.ModelAdmin):
    list_display = ("value", "label")

class ViewabilityAdmin(admin.ModelAdmin):
    list_display = ("value", "label")

class target_typeAdmin(admin.ModelAdmin):
    list_display = ("category", "subcategory")


class LocationAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "city", "tier", "population")
    search_fields = ("country",)
    list_filter = ("country",)
    ordering = ("country",)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "objective", "start_time", "end_time", "status")
    search_fields = ("name", "objective", "status")
    list_filter = ("name", "objective", "status")
    ordering = ("name", "objective", "status")


admin.site.register(UserType, UserTypeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Campaign,CampaignAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(target_type, target_typeAdmin)
admin.site.register(CampaignImage)
admin.site.register(Keyword)
admin.site.register(Age)
admin.site.register(CarrierData, CarrierDataAdmin)
admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Impression)
admin.site.register(DevicePrice)
admin.site.register(Device)
admin.site.register(DistinctInterest)
admin.site.register(CampaignVideo)
admin.site.register(BrandSafety, BrandSafetyAdmin)
admin.site.register(BuyType, BuyTypeAdmin)
admin.site.register(Bidding_detail)
admin.site.register(Viewability, ViewabilityAdmin)

@admin.register(CityData)
class CityDataAdmin(admin.ModelAdmin):
    list_display = ("city", "state", "country", "tier", "city_population")
    search_fields = ("city", "state", "country", "tier")
