from django.urls import path, re_path
from . import views
from .views import HomeView, SignUpView, LoginView, VerifyPassword, RefreshAccessTokenView, VerifyOTPView
from authentication.services.Serializers import CustomTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('home/', HomeView.as_view(), name='api_home'),
    path('signup/', SignUpView.as_view(), name='api_signup'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('verify/', VerifyPassword.as_view(), name="api_verify"),
    path('refresh-access-token/', RefreshAccessTokenView.as_view(), name="api_refresh_token"),
    path('otp/', VerifyOTPView.as_view(), name="api_verify"),
]
