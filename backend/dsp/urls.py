"""
URL configuration for dsp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import RegisterView, GoogleLoginView,home, CustomTokenObtainPairView, LogoutView, ForgotPasswordView,UpdatePasswordView,UpdateProfileView,CampaignView, DuplicateCampaignView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/google-login/", GoogleLoginView.as_view(), name="google_login"),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('', home, name='home'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/update-password/', UpdatePasswordView.as_view(), name='update_password'),
    path('api/update-profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('campaigns/', CampaignView.as_view(), name='create_campaign'),
    path('campaigns/<int:pk>/', CampaignView.as_view(), name='edit_campaign'),
    path('campaigns/<int:pk>/duplicate/', DuplicateCampaignView.as_view(), name='duplicate_campaign'),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
