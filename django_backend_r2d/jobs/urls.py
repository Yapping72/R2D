from django.urls import path
from jobs.views import JobSaveView

urlpatterns = [
    # Other URL patterns...
    path('save/', JobSaveView.as_view(), name='save-job'),
]
