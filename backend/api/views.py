import logging

from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import pandas as pd
from rest_framework.views import APIView
from django.http import HttpResponse

from .models import (Campaign, CampaignImage, Keyword, Location, proximity, CampaignVideo,
                     proximity_store, target_type, weather, UserType, Age, CarrierData,
    Environment,
    Exchange,
    Language,
    Impression,
    DevicePrice,
    Device,
    DistinctInterest,Bidding_detail, BrandSafety,
    BuyType,
    Viewability,tag_tracker)
from .serializers import (CampaignCreateUpdateSerializer,
                          CampaignImageSerializer, CampaignSerializer,
                          KeywordSerializer, LocationSerializer,
                          ProximitySerializer, ProximityStoreSerializer,
                          WeatherSerializer, target_typeSerializer,BiddingDetailsSerializer,CampaignVideoSerializer,tag_trackerSerializer)

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

@api_view(['POST'])
def login_page(request):
    payload = request.data
    audience_list = payload['data'][0]
    for item in audience_list:
        category = item.get("category")
        subcategory = item.get("subcategory")
        target_type.objects.create(category=category,subcategory=subcategory)
    return Response({"message": "Target type created successfully"}, status=status.HTTP_200_OK)




def serializer_data_to_csv(serializer_data):
    """
    Convert a list of dicts (serializer data) into CSV format using pandas
    and return the CSV as a string.
    """
    df = pd.DataFrame(serializer_data)
    csv_string = df.to_csv(index=False)
    return csv_string



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


class CampaignVideoViewSet(viewsets.ModelViewSet):
    queryset = CampaignVideo.objects.all()
    serializer_class = CampaignVideoSerializer



class BiddingDetailsViewSet(viewsets.ModelViewSet):
    queryset = Bidding_detail.objects.all()
    serializer_class = BiddingDetailsSerializer



class ProximityStoreViewSet(viewsets.ModelViewSet):
    queryset = proximity_store.objects.all()
    serializer_class = ProximityStoreSerializer


class ProximityViewSet(viewsets.ModelViewSet):
    queryset = proximity.objects.all()
    serializer_class = ProximitySerializer


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = weather.objects.all()
    serializer_class = WeatherSerializer

class tag_trackerViewSet(viewsets.ModelViewSet):
    queryset = tag_tracker.objects.all()
    serializer_class = tag_trackerSerializer


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class CampaignPagination(PageNumberPagination):
    page_size = 10  # Set default page size
    page_size_query_param = "page_size"  # Allow the user to specify the page size
    max_page_size = 100

@api_view(["GET"])
def age_api(request):
    age_queryset = Age.objects.all()
    data = []
    for age in age_queryset:
        data.append({"id": age.id,"value": age.age , "label" : age.label})
    return success_response("Data succcessfully fetched", data)

@api_view(["GET"])
def brandSafety_api(request):
    age_queryset = BrandSafety.objects.all()
    data = []
    for age in age_queryset:
        data.append({"id": age.id, "value": int(age.value) , "label" : age.label})
    return success_response("Data succcessfully fetched", data)

@api_view(["GET"])
def Viewability_api(request):
    age_queryset = Viewability.objects.all()
    data = []
    for age in age_queryset:
        data.append({"id": age.id, "value": int(age.value) , "label" : age.label})
    return success_response("Data succcessfully fetched", data)

@api_view(["GET"])
def BuyType_api(request):
    age_queryset = BuyType.objects.all()
    data = []
    for age in age_queryset:
        data.append({"id": age.id, "value": age.value , "label" : age.label})
    return success_response("Data succcessfully fetched", data)


@api_view(["GET"])
def DevicePrice_api(request):
    age_queryset = DevicePrice.objects.all()
    data = []
    for age in age_queryset:
        data.append({"id": age.id,"value": age.price, "label" : age.label})
    return success_response("Data succcessfully fetched", data)

@api_view(["GET"])
def Device_api(request):
    age_queryset = Device.objects.all()
    data = []
    for age in age_queryset:
        data.append({"id": age.id, "value": age.device,  "label" : age.label})
    return success_response("Data succcessfully fetched", data)

@api_view(["GET"])
def DistinctInterest_api(request):
    age_queryset = DistinctInterest.objects.all()
    data = []
    for age in age_queryset:
        data.append({"id": age.id,"value": age.interest,  "label" : age.label})
    return success_response("Data succcessfully fetched", data)

@api_view(["GET"])
def CarrierData_api(request):
    age_queryset = CarrierData.objects.all()
    data = []
    for age in age_queryset:
        data.append({"id": age.id,"value": age.carrier,  "label" : age.label})
    return success_response("Data succcessfully fetched", data)

@api_view(["GET"])
def Environment_api(request):
    age_queryset = Environment.objects.all()
    data = []
    for age in age_queryset:
        data.append({"id": age.id,"value": age.env, "label" : age.label})
    return success_response("Data succcessfully fetched", data)

@api_view(["GET"])
def Exchange_api(request):
    age_queryset = Exchange.objects.all()
    data = []
    for age in age_queryset:
        data.append({"id": age.id,"value": age.exchange, "label" : age.label})
    return success_response("Data succcessfully fetched", data)

@api_view(["GET"])
def Language_api(request):
    age_queryset = Language.objects.all()
    data = []
    for age in age_queryset:
        data.append({"id": age.id,"value": age.language , "iso_code" : age.iso_code ,  "label" : age.label})
    return success_response("Data succcessfully fetched", data)

@api_view(["GET"])
def Impression_api(request):
    age_queryset = Impression.objects.all()
    data = []
    for age in age_queryset:
        data = age.impression
    return Response(data)

class FileGetView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Campaign.objects.all()
        serializer = CampaignSerializer(queryset, many=True)
        serializer_data = serializer.data
        csv_data = serializer_data_to_csv(serializer_data)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="my_data.csv"'
        response.write(csv_data)
        return response
    
    def post(self, request, *args, **kwargs):
        """
        POST: Upload a CSV file to create/update MyModel records.
        Expecting a 'file' field in multipart/form-data.
        """
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({'error': 'No file was uploaded.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            return Response({'error': f'Failed to read CSV file: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)

        created_count = 0
        for index, row in df.iterrows():
            print("hello")
            #Campaign.objects.filter(id=row.get('id')).update(viewability=value,impressions=,clicks=,ctr=,views=,vtr=)


        return Response(
            {'message': f'Successfully created {created_count} records.'},
            status=status.HTTP_201_CREATED
        )

from django.db.models import Q
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetch_user_campgain(request):

    query_param = request.query_params.get("query", None)

    user_type_pm_values = UserType.objects.filter(user=request.user).values_list('user_type_pm', flat=True)

    if query_param:
        query_values = [value.strip() for value in query_param.split(",")]
        query = Q()
        for value in query_values:
            query |= (
            Q(name__icontains=value) |
            Q(user__username__icontains=value) |
            Q(user__email__icontains=value) |
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value)
        )
        queryset = Campaign.objects.filter(query)
    elif user_type_pm_values.first() is True:
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
        queryset = target_type.objects.filter(category__in=query_values)
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
