from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (Campaign, CampaignImage, Keyword, Location, UserType,
                     proximity, proximity_store, target_type, weather, UserProfile)


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            try:
                user = User.objects.get(email=username)
                if not user.check_password(password):
                    user = None
            except User.DoesNotExist:
                user = None

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        user_type = False
        user_type = UserType.objects.get(user=user)
        if user_type.user_type_pm is True:
            user_type = True
        else:
            user_type = False
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_type": user_type,
        }


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

    def validate_email(self, value):
        # Ensure the email is unique for other users
        if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["city", "phone_no"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "date_joined", "profile"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = self.context["request"].user
        if not user.check_password(data["old_password"]):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct."}
            )
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError(
                {"confirm_new_password": "Passwords do not match."}
            )
        try:
            validate_password(data["new_password"], user)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})
        return data

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "country", "state", "city", "tier", "population"]


class target_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = target_type
        fields = ["id", "targeting_type", "category"]


# Serializers
class CampaignImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignImage
        fields = ["id", "image", "created_at"]


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["id", "file", "keywords"]

    def validate(self, data):
        # Check if both 'file' and 'keywords' are empty
        if not data.get("file") and not data.get("keywords"):
            raise serializers.ValidationError(
                "Either 'file' or 'keywords' must be provided."
            )
        return data


class ProximityStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = proximity_store
        fields = ["id", "file"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].required = True


class ProximitySerializer(serializers.ModelSerializer):
    class Meta:
        model = proximity
        fields = ["id", "file"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].required = True


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = weather
        fields = ["id", "file"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].required = True


class CampaignSerializer(serializers.ModelSerializer):
    images = CampaignImageSerializer(many=True, read_only=True)
    keywords = KeywordSerializer(many=True, read_only=True)
    proximity_store = ProximityStoreSerializer(many=True, read_only=True)
    proximity = ProximitySerializer(many=True, read_only=True)
    weather = WeatherSerializer(many=True, read_only=True)
    location = LocationSerializer(many=True, read_only=True)
    target_type = target_typeSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = "__all__"


class CampaignCreateUpdateSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CampaignImage.objects.all(), required=False
    )
    keywords = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Keyword.objects.all(), required=False
    )
    target_type = serializers.PrimaryKeyRelatedField(
        many=True, queryset=target_type.objects.all(), required=False
    )

    location = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Location.objects.all(), required=False
    )
    proximity_store = serializers.PrimaryKeyRelatedField(
        many=True, queryset=proximity_store.objects.all(), required=False
    )
    proximity = serializers.PrimaryKeyRelatedField(
        many=True, queryset=proximity.objects.all(), required=False
    )
    weather = serializers.PrimaryKeyRelatedField(
        many=True, queryset=weather.objects.all(), required=False
    )

    class Meta:
        model = Campaign
        fields = "__all__"

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        keywords = validated_data.pop("keywords", [])
        location = validated_data.pop("location", [])
        proximity_store = validated_data.pop("proximity_store", [])
        proximity = validated_data.pop("proximity", [])
        weather = validated_data.pop("weather", [])
        target_type = validated_data.pop("target_type", [])

        campaign = Campaign.objects.create(**validated_data)
        campaign.location.set(location)
        campaign.images.set(images)
        campaign.keywords.set(keywords)
        campaign.proximity_store.set(proximity_store)
        campaign.proximity.set(proximity)
        campaign.weather.set(weather)
        campaign.target_type.set(target_type)
        return campaign


class UserUpdateSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="profile.city", required=False)
    phone_no = serializers.CharField(source="profile.phone_no", required=False)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "city", "phone_no"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()

        profile = instance.profile
        profile.city = profile_data.get("city", profile.city)
        profile.phone_no = profile_data.get("phone_no", profile.phone_no)
        profile.save()

        return instance
