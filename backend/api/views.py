import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from .models import Campaign,CampaignImage, CampaignLogo, TargetDemographic, Keyword, Topic, Location, proximity_store, proximity, weather
from .serializers import  CampaignCreateUpdateSerializer,CampaignSerializer, CampaignImageSerializer, CampaignLogoSerializer,TargetDemographicSerializer,KeywordSerializer,TopicSerializer,LocationSerializer, ProximitySerializer, WeatherSerializer, ProximityStoreSerializer
from django.shortcuts import render
from rest_framework import viewsets, status
logger = logging.getLogger(__name__)
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

def home(request):
    return render(request, "dsp/index.html")



class CampaignViewSet(viewsets.ViewSet):
    
    def list(self, request):
        """List all campaigns with related data."""
        queryset = Campaign.objects.all()
        serializer = CampaignSerializer(queryset, many=True)
        return success_response("Campaign List", serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieve a campaign by ID."""
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignSerializer(campaign)
        return success_response("Campaign List",serializer.data)

    def create(self, request):
        """Create a new campaign."""
        serializer = CampaignCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return success_response("Campaign Successfully created", serializer.data)
        return error_response(serializer.errors)

    def update(self, request, pk=None):
        """Update an existing campaign."""
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignCreateUpdateSerializer(campaign, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return success_response("Campaign Successfully updated", serializer.data)
        return error_response(serializer.errors)

    def partial_update(self, request, pk=None):
        """Partially update a campaign."""
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignCreateUpdateSerializer(campaign, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return success_response("Campaign Successfully created", serializer.data)
        return error_response(serializer.errors)

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

class ProximityStoreViewSet(viewsets.ModelViewSet):
    queryset = proximity_store.objects.all()
    serializer_class = ProximityStoreSerializer

class ProximityViewSet(viewsets.ModelViewSet):
    queryset = proximity.objects.all()
    serializer_class = ProximitySerializer

class WeatherViewSet(viewsets.ModelViewSet):
    queryset = weather.objects.all()
    serializer_class = WeatherSerializer



class TargetDemographicViewSet(viewsets.ModelViewSet):
    queryset = TargetDemographic.objects.all()
    serializer_class = TargetDemographicSerializer

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetch_user_campgain(request):
    queryset = Campaign.objects.filter(user=request.user)
    serializer = CampaignSerializer(queryset, many=True)
    return success_response("Data succcessfully fetched", serializer.data)

@api_view(["GET"])
def location(request):
    queryset = Location.objects.all()
    serializer = LocationSerializer(queryset, many=True)
    return success_response("Data succcessfully fetched", serializer.data)



