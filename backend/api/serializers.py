from rest_framework import serializers
from django.contrib.auth.models import User
import secrets
import string
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email as django_validate_email
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserType

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
            "user_type" : user_type
        }
    
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def validate_email(self, value):
        # Ensure the email is unique for other users
        if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value



from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Campaign, CampaignImage, CampaignLogo, TargetDemographic, Keyword, Topic

# Serializers
class CampaignImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignImage
        fields = ['id', 'image', 'created_at']

class CampaignLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignLogo
        fields = ['id', 'logo', 'created_at']

class TargetDemographicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetDemographic
        fields = ['id', 'name']

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'keyword']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'topic']

class CampaignSerializer(serializers.ModelSerializer):
    images = CampaignImageSerializer(many=True, read_only=True)
    logos = CampaignLogoSerializer(many=True, read_only=True)
    target_demographics = TargetDemographicSerializer(many=True, read_only=True)
    keywords = KeywordSerializer(many=True, read_only=True)
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = '__all__'

class CampaignCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


