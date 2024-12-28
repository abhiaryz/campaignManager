from rest_framework import serializers
from django.contrib.auth.models import User

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def validate_email(self, value):
        # Ensure the email is unique for other users
        if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value

from rest_framework import serializers
from .models import Campaign

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'
