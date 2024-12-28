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
from .models import Campaign
from .serializers import CampaignSerializer, UpdateProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
logger = logging.getLogger(__name__)


# Utility Functions
def success_response(message, data=None, status_code=status.HTTP_200_OK):
    """Utility for generating a consistent success response."""
    return Response({"message": message, "data": data}, status=status_code)


def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    """Utility for generating a consistent error response."""
    return Response({"error": message}, status=status_code)


# Home Page
def home(request):
    return render(request, "dsp/index.html")


# Register View
class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Register a new user",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_QUERY, description="Username of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('password', openapi.IN_QUERY, description="Password of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('email', openapi.IN_QUERY, description="Email of the user", type=openapi.TYPE_STRING),
        ],
        responses={201: "User  created successfully", 400: "Bad Request"}
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not username or not password or not email:
            return error_response("All fields are required.")

        if User.objects.filter(username=username).exists():
            return error_response("Username already exists.")

        try:
            user = User.objects.create_user(
                username=username, password=password, email=email
            )
            return success_response("User created successfully.", {"id": user.id}, status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return error_response("Failed to create user.")


# Google Login View
class GoogleLoginView(APIView):
    @swagger_auto_schema(
        operation_description="Login using Google OAuth",
        manual_parameters=[
            openapi.Parameter('token', openapi.IN_QUERY, description="Google OAuth token", type=openapi.TYPE_STRING),
        ],
        responses={200: "Login successful", 400: "Bad Request"}
    )
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return error_response("Token is required.")

        try:
            strategy = load_strategy(request)
            backend = load_backend(strategy=strategy, name="google-oauth2", redirect_uri=None)
            user = backend.do_auth(token)

            if user and user.is_active:
                refresh = RefreshToken.for_user(user)
                return success_response("Login successful.", {"refresh": str(refresh), "access": str(refresh.access_token)})
            return error_response("Authentication failed.")
        except (MissingBackend, AuthTokenError) as e:
            logger.error(f"Google login error: {e}")
            return error_response("Invalid token or backend.")


# Logout View
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


# Forgot Password View
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


# Update Password View
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


# Update Profile View
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UpdateProfileSerializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return success_response("Profile updated successfully.", serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Campaign View
class CampaignView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new campaign",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Name of the campaign", type=openapi.TYPE_STRING),
            openapi.Parameter('campaign_type', openapi.IN_QUERY, description="Type of the campaign", type=openapi.TYPE_STRING),
            openapi.Parameter('text', openapi.IN_QUERY, description="Text for the campaign", type=openapi.TYPE_STRING),
            openapi.Parameter('geo_location', openapi.IN_QUERY, description="Geographical location", type=openapi.TYPE_STRING),
            openapi.Parameter('price', openapi.IN_QUERY, description="Price of the campaign", type=openapi.TYPE_NUMBER),
            openapi.Parameter('file', openapi.IN_QUERY, description="File associated with the campaign", type=openapi.TYPE_FILE),
        ],
        responses={201: "Campaign created successfully", 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Campaign created successfully.", serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignSerializer(instance=campaign, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response("Campaign updated successfully.", serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignSerializer(campaign)
        return success_response("Campaign retrieved successfully.", serializer.data)


# Duplicate Campaign View
class DuplicateCampaignView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new campaign",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Name of the campaign", type=openapi.TYPE_STRING),
            openapi.Parameter('campaign_type', openapi.IN_QUERY, description="Type of the campaign", type=openapi.TYPE_STRING),
            openapi.Parameter('text', openapi.IN_QUERY, description="Text for the campaign", type=openapi.TYPE_STRING),
            openapi.Parameter('geo_location', openapi.IN_QUERY, description="Geographical location", type=openapi.TYPE_STRING),
            openapi.Parameter('price', openapi.IN_QUERY, description="Price of the campaign", type=openapi.TYPE_NUMBER),
            openapi.Parameter('file', openapi.IN_QUERY, description="File associated with the campaign", type=openapi.TYPE_FILE),
        ],
        responses={201: "Campaign created successfully", 400: "Bad Request"}
    )
    def post(self, request, pk):
        campaign = get_object_or_404(Campaign, pk=pk)
        original_data = CampaignSerializer(campaign).data
        original_data.pop("id")  # Remove the ID to create a new instance
        new_campaign = Campaign.objects.create(**original_data)
        serializer = CampaignSerializer(new_campaign)
        return success_response("Campaign duplicated successfully.", serializer.data)
