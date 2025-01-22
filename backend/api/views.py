import logging

from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (Campaign, CampaignImage, Keyword, Location, proximity,
                     proximity_store, target_type, weather, UserType)
from .serializers import (CampaignCreateUpdateSerializer,
                          CampaignImageSerializer, CampaignSerializer,
                          KeywordSerializer, LocationSerializer,
                          ProximitySerializer, ProximityStoreSerializer,
                          WeatherSerializer, target_typeSerializer)

logger = logging.getLogger(__name__)


# Utility Functions
def success_response(message, data=None, status_code=status.HTTP_200_OK):
    """Utility for generating a consistent success response."""
    return Response(
        {"message": message, "data": data, "success": True}, status=status_code
    )


def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    """Utility for generating a consistent error response."""
    return Response(
        {"message": message, "success": False, "data": []}, status=status_code
    )


def login_page(request):
    return render(request, "dsp/login.html")


def register_page(request):
    return render(request, "dsp/register.html")


def forgot_password_page(request):
    return render(request, "dsp/forgot_password.html")


def home(request):
    return render(request, "dsp/index.html")


def campaigns_page(request):
    return render(request, "dsp/campaigns.html")


def add_campaign_page(request):
    return render(request, "dsp/add_campaigns.html")


def dashboard_profile(request):
    return render(request, "dsp/profile.html")


def dashboard_data(request):
    return render(request, "dsp/data.html")


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
        return success_response("Campaign List", serializer.data)

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
        serializer = CampaignCreateUpdateSerializer(
            campaign, data=request.data, partial=False
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return success_response("Campaign Successfully updated", serializer.data)
        return error_response(serializer.errors)

    def partial_update(self, request, pk=None):
        """Partially update a campaign."""
        campaign = get_object_or_404(Campaign, pk=pk)
        serializer = CampaignCreateUpdateSerializer(
            campaign, data=request.data, partial=True
        )
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


class ProximityStoreViewSet(viewsets.ModelViewSet):
    queryset = proximity_store.objects.all()
    serializer_class = ProximityStoreSerializer


class ProximityViewSet(viewsets.ModelViewSet):
    queryset = proximity.objects.all()
    serializer_class = ProximitySerializer


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = weather.objects.all()
    serializer_class = WeatherSerializer


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class CampaignPagination(PageNumberPagination):
    page_size = 10  # Set default page size
    page_size_query_param = "page_size"  # Allow the user to specify the page size
    max_page_size = 100


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetch_user_campgain(request):
    user_type_pm_values = UserType.objects.filter(user=request.user).values_list('user_type_pm', flat=True)
    if user_type_pm_values.first() is True:
        queryset = Campaign.objects.all().order_by("-updated_at")
    else:
        queryset = Campaign.objects.filter(user=request.user).order_by("-updated_at")

    paginator = CampaignPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serializer = CampaignSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(
        {
            "message": "Data successfully fetched",
            "data": serializer.data,
            "success": True,
        }
    )


@api_view(["GET"])
def location(request):
    queryset = Location.objects.all()
    serializer = LocationSerializer(queryset, many=True)
    return success_response("Data succcessfully fetched", serializer.data)


@api_view(["GET"])
def target_type_view(request):
    query_param = request.query_params.get("query", None)

    if query_param == "unique":
        # Get distinct values of 'targeting_type'
        queryset = target_type.objects.values("targeting_type").distinct()
        return Response(
            {
                "message": "Unique targeting types fetched successfully",
                "data": list(queryset),
            }
        )
    elif query_param:
        query_values = [value.strip() for value in query_param.split(",")]

        # Filter the queryset for each value in the query_values list
        queryset = target_type.objects.filter(targeting_type__in=query_values)
        if queryset.exists():
            serializer = target_typeSerializer(queryset, many=True)
            return Response(
                {
                    "message": "Data successfully fetched for the given targeting_type",
                    "data": serializer.data,
                }
            )
        else:
            return Response(
                {
                    "message": f"No results found for targeting_type: {query_param}",
                    "data": [],
                }
            )
    else:
        # Default behavior: return all target_type objects if no query parameter
        queryset = target_type.objects.all()
        serializer = target_typeSerializer(queryset, many=True)
        return Response(
            {"message": "Data successfully fetched", "data": serializer.data}
        )
