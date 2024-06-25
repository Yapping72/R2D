from django.urls import path
from jobs.views import JobSaveView, UpdateJobStatusView

urlpatterns = [
    path('save/', JobSaveView.as_view(), name='save-job'), # URL pattern for saving a job
    path('update-status/', UpdateJobStatusView.as_view(), name='update-job-status') # URL pattern for updating job status
]
