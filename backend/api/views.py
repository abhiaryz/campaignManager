from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import load_strategy
from social_django.utils import load_backend
from social_core.exceptions import MissingBackend, AuthTokenError

from django.shortcuts import render

def home(request):
    return render(request, 'dsp/index.html')

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        if not username or not password or not email:
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        user.save()
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )


class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response(
                {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        strategy = load_strategy(request)
        try:
            backend = load_backend(
                strategy=strategy, name="google-oauth2", redirect_uri=None
            )
            user = backend.do_auth(token)
        except MissingBackend:
            return Response(
                {"error": "Invalid backend"}, status=status.HTTP_400_BAD_REQUEST
            )
        except AuthTokenError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(
            {"error": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST
        )
