from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import auth, profile, views

router = DefaultRouter()
router.register(r"campaigns", views.CampaignViewSet, basename="campaign")
router.register(
    r"campaign-images", views.CampaignImageViewSet, basename="campaign-image"
)
router.register(r"keywords", views.KeywordViewSet, basename="keyword")
router.register(
    r"proximityStore", views.ProximityStoreViewSet, basename="proximityStore"
)
router.register(r"proximity", views.ProximityViewSet, basename="proximity")
router.register(r"weather", views.WeatherViewSet, basename="weather")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", auth.RegisterView.as_view(), name="register"),
    path("api/logout/", auth.LogoutView.as_view(), name="logout"),
    path(
        "api/forgot-password/",
        auth.ForgotPasswordView.as_view(),
        name="forgot_password",
    ),
    path(
        "api/user/change-password/",
        auth.ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    path("", views.home, name="home"),
    path(
        "api/update-password/",
        auth.UpdatePasswordView.as_view(),
        name="update_password",
    ),
    path(
        "api/user/update/", profile.UserUpdateAPIView.as_view(), name="update_profile"
    ),
    path(
        "api/token/", auth.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/",
        auth.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/token/verify/", auth.CustomTokenVerifyView.as_view(), name="token_verify"
    ),
    path(
        "api/fetch_user_campgain/",
        views.fetch_user_campgain,
        name="fetch_user_campgain",
    ),
    path("api/location/", views.location, name="location"),
    path("api/profile/", profile.profile_api, name="profile"),
    path("api/users/", profile.UserAPIView.as_view(), name="user-list"),
    path("api/users/<int:pk>/", profile.UserAPIView.as_view(), name="user-detail"),
    path("api/", include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
