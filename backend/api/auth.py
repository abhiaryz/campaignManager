import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import load_backend, load_strategy
from social_core.exceptions import MissingBackend, AuthTokenError
from .models import Campaign,UserType,CampaignImage, CampaignLogo, TargetDemographic, Keyword, Topic, Location
from .serializers import  UpdateProfileSerializer,CustomTokenObtainPairSerializer,CampaignCreateUpdateSerializer,CampaignSerializer, CampaignImageSerializer, CampaignLogoSerializer,TargetDemographicSerializer,KeywordSerializer,TopicSerializer,LocationSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
from rest_framework import serializers, viewsets, status
logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserUpdateSerializer
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ChangePasswordSerializer
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
# Utility Functions
def success_response(message, data=None, status_code=status.HTTP_200_OK):
    """Utility for generating a consistent success response."""
    return Response({"message": message, "data": data, "success": True}, status=status_code)


def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    """Utility for generating a consistent error response."""
    return Response({"message": message,"success": False, "data": []}, status=status_code)

class RegisterView(APIView):

    def post(self, request):
        password = request.data.get("password")
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        username = email
        if not username or not password or not email:
            return error_response("All fields are required.")

        if User.objects.filter(username=username).exists():
            return error_response("Username already exists.")

        try:
            user = User.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name
            )
            UserType.objects.create(user=user)
            return success_response("User created successfully.", {"id": user.id}, status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return error_response("Failed to create user.")

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return error_response("Refresh token is required.")

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return success_response("Logout successful.")
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return error_response("Invalid token.")

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return error_response("Email is required.")

        user = User.objects.filter(email=email).first()
        if not user:
            return error_response("No user found with this email.", status.HTTP_404_NOT_FOUND)

        try:
            reset_link = f"http://example.com/reset-password/{user.id}/"  # Replace with actual frontend link
            send_mail(
                subject="Password Reset Request",
                message=f"Hi {user.username},\n\nUse the following link to reset your password:\n{reset_link}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
            return success_response("Password reset link sent to your email.")
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")
            return error_response("Failed to send email.")

class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password or not new_password:
            return error_response("Both current_password and new_password are required.")

        if len(new_password) < 8:
            return error_response("New password must be at least 8 characters long.")

        user = request.user
        if not user.check_password(current_password):
            return error_response("Current password is incorrect.")

        user.set_password(new_password)
        user.save()
        return success_response("Password updated successfully.")

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return success_response("Password updated successfully", serializer.data)
        return error_response(serializer.errors)

class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"status": status.HTTP_200_OK, "data": serializer.validated_data},
                status=status.HTTP_200_OK,
            )
        return error_response(
            serializer.errors
        )