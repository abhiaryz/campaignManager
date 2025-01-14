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

def success_response(message, data=None, status_code=status.HTTP_200_OK):
    """Utility for generating a consistent success response."""
    return Response({"message": message, "data": data, "success": True}, status=status_code)


def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    """Utility for generating a consistent error response."""
    return Response({"message": message,"success": False, "data": []}, status=status_code)

class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_api(request):
    data = {"id":  request.user.id,"username": request.user.username,"first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,}
    return success_response("Data succcessfully fetched", data)