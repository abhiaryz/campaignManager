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
    Viewability,tag_tracker,CampaignFile)
from .serializers import (CampaignCreateUpdateSerializer,
                          CampaignImageSerializer, CampaignSerializer,
                          KeywordSerializer, LocationSerializer,
                          ProximitySerializer, ProximityStoreSerializer,
                          WeatherSerializer, target_typeSerializer,BiddingDetailsSerializer,CampaignVideoSerializer,tag_trackerSerializer)
import xlsxwriter
from django.core.files.base import File

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

import io
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

from .models import Campaign
from .serializers import CampaignSerializer

from io import BytesIO

def serializer_data_to_excel(serializer_data):
    # If serializer_data is a dict (for a single record), wrap it in a list.
    if isinstance(serializer_data, dict):
        data = [serializer_data]
    else:
        data = serializer_data  # Assuming it's already a list of dicts

    # Create a DataFrame from the data.
    df = pd.DataFrame(data)
    
    columns_to_remove = ['images', 'keywords', 'proximity_store', 'proximity', 'weather', 'target_type', 'location', 'video', 'tag_tracker','age','carrier_data','environment','exchange','language','impression','device_price','device','created_at','updated_at','carrier','landing_page','reports_url','start_time','end_time','status','day_part','objective','user']

    # Drop these columns if they exist (ignore if they don't)
    df.drop(columns=columns_to_remove, inplace=True, errors='ignore')
    # Convert DataFrame to an Excel file in memory.
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output



class FileGetView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Query all Campaign objects for the current user
        campaigns = Campaign.objects.all()
        
        # Prepare a list to hold the response data
        response_data = []

        # Process each campaign individually.
        for campaign in campaigns:
            # Check if a CampaignFile already exists for this campaign.
            campaign_file_qs = CampaignFile.objects.filter(campaign=campaign)
            if campaign_file_qs.exists():
                # If a file exists, get it (you can choose to get the first or handle multiple)
                campaign_file = campaign_file_qs.first()
                response_data.append({
                    'campaign_id': campaign.id,
                    'file_url': campaign_file.file.url,  # You can return the URL or any file data
                    'status': 'exists'
                })
            else:
                # If no file exists for the campaign, create one.
                serializer = CampaignSerializer(campaign)
                serializer_data = serializer.data

                # Convert the serializer data to Excel data.
                excel_data = serializer_data_to_excel(serializer_data)
                excel_data.seek(0)  # Reset the stream pointer to the beginning

                file_name = f"campaign_{campaign.id}.xlsx"
                django_file = File(excel_data, name=file_name)
                
                # Create the CampaignFile record
                campaign_file = CampaignFile.objects.create(campaign=campaign, file=django_file)
                
                response_data.append({
                    'campaign_id': campaign.id,
                    'file_url': campaign_file.file.url,
                    'status': 'created'
                })
        
        return Response(response_data, status=status.HTTP_200_OK)
       

    def post(self, request, *args, **kwargs):
        """
        POST: Upload an Excel file (.xlsx) to update a particular Campaign record.
        The campaign id should be provided in the URL (e.g. /campaign/<int:campaign_id>/upload/).
        
        The Excel file (Sheet1) is expected to contain columns like:
          id, name, total_budget, viewability, brand_safety, impressions,
          clicks, ctr, views, vtr, buy_type, unit_rate
          
        For the campaign specified, the view aggregates the columns:
          - viewability, impressions, clicks, ctr, views, and vtr
        and then updates the Campaign model with these totals.
        """
        # 1. Get the campaign id from the URL
        campaign_id = self.kwargs.get('campaign_id')
        if not campaign_id:
            return Response({'error': 'Campaign ID not provided in URL.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Ensure the campaign exists
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({'error': 'Campaign not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        
        # 3. Get the Excel file from the request
        excel_file = request.FILES.get('file')
        if not excel_file:
            return Response({'error': 'No file was uploaded.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # 4. Read the Excel file (from sheet 1)
        try:
            df = pd.read_excel(excel_file, sheet_name=0)
        except Exception as e:
            return Response({'error': f'Failed to read Excel file: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # 5. Verify that the Excel file contains a column for the campaign ID.
        if 'id' not in df.columns:
            return Response({'error': 'Excel file must contain a column named "id".'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Filter the DataFrame to include only rows for the provided campaign ID.
        df = df[df['id'] == campaign_id]
        if df.empty:
            return Response({'error': 'No rows in Excel file match the provided campaign id.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # 6. Aggregate (sum) the required columns. (You can adjust which columns to aggregate as needed.)
        total_viewability = df['viewability'].sum() if 'viewability' in df.columns else 0
        total_impressions = df['impressions'].sum() if 'impressions' in df.columns else 0
        total_clicks = df['clicks'].sum() if 'clicks' in df.columns else 0
        total_ctr = df['ctr'].sum() if 'ctr' in df.columns else 0
        total_views = df['views'].sum() if 'views' in df.columns else 0
        total_vtr = df['vtr'].sum() if 'vtr' in df.columns else 0
        
        # Optionally, log the aggregated values for debugging.
        print(f"Aggregated totals for campaign {campaign_id}:")
        print(f"  Viewability: {total_viewability}")
        print(f"  Impressions: {total_impressions}")
        print(f"  Clicks: {total_clicks}")
        print(f"  CTR: {total_ctr}")
        print(f"  Views: {total_views}")
        print(f"  VTR: {total_vtr}")
        
        # 7. Update the Campaign record with the aggregated totals.
        Campaign.objects.filter(id=campaign_id).update(
            viewability=total_viewability,
            impressions=total_impressions,
            clicks=total_clicks,
            ctr=total_ctr,
            views=total_views,
            vtr=total_vtr,
        )
        
        processed_count = len(df)  # Number of rows aggregated
        
        return Response(
            {'message': f'Successfully processed {processed_count} Excel rows and updated Campaign {campaign_id}.'},
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
        queryset = Campaign.objects.filter(query).order_by("-updated_at")
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
