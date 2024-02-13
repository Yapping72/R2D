from django.urls import path
from accounts.views import DRFStatusView

urlpatterns = [
    path('drf-status/', DRFStatusView.as_view(), name='drf-status'),
]
