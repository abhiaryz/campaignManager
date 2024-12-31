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
from .models import Campaign,UserType,CampaignImage, CampaignLogo, TargetDemographic, Keyword, Topic
from .serializers import  UpdateProfileSerializer,CustomTokenObtainPairSerializer,CampaignCreateUpdateSerializer,CampaignSerializer, CampaignImageSerializer, CampaignLogoSerializer,TargetDemographicSerializer,KeywordSerializer,TopicSerializer
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




class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ViewSets
class CampaignViewSet(viewsets.ViewSet):
    
    def list(self, request):
        """List all campaigns with related data."""
        queryset = Campaign.objects.all()
        serializer = CampaignSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieve a campaign by ID."""
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignSerializer(campaign)
        return Response(serializer.data)

    def create(self, request):
        """Create a new campaign."""
        serializer = CampaignCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Update an existing campaign."""
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignCreateUpdateSerializer(campaign, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """Partially update a campaign."""
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignCreateUpdateSerializer(campaign, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a campaign."""
        campaign = get_object_or_404(Campaign, pk=pk)
        campaign.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CampaignImageViewSet(viewsets.ModelViewSet):
    queryset = CampaignImage.objects.all()
    serializer_class = CampaignImageSerializer

class CampaignLogoViewSet(viewsets.ModelViewSet):
    queryset = CampaignLogo.objects.all()
    serializer_class = CampaignLogoSerializer

class TargetDemographicViewSet(viewsets.ModelViewSet):
    queryset = TargetDemographic.objects.all()
    serializer_class = TargetDemographicSerializer

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TestEmailView(APIView):
    def post(self, request):
        """
        Send a test email based on the provided data.
        """
        recipient = request.data.get('recipient')  # Email address of the recipient
        subject = request.data.get('subject', 'Test Email')  # Default subject
        message = request.data.get('message', 'This is a test email.')  # Default message

        if not recipient:
            return Response(
                {"error": "Recipient email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

       
        email = EmailMessage(
                subject=subject,
                body=message,
                from_email='aryzabhishek@gmail.com',  # Replace with your email
                to=[recipient],
            )    
        email.send()
        return Response(
                {"message": f"Test email sent successfully to {recipient}."},
                status=status.HTTP_200_OK,
            )
            


class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"status": status.HTTP_200_OK, "data": serializer.validated_data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": {
                    "code": "",
                    "data": serializer.errors,
                    "type": "Auth Error",
                    "message": "Authentication failed. Please check your credentials and try again.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )