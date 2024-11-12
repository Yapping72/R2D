from django.urls import path
from jobs.views import JobSaveView, UpdateJobStatusView, GetOneJobView, GetAllJobsView, GetJobHistoryView, GetCompletedJobsView, DeleteJobsView

urlpatterns = [
    path('save/', JobSaveView.as_view(), name='save-job'), # URL pattern for saving a job
    path('update-status/', UpdateJobStatusView.as_view(), name='update-job-status'), # URL pattern for updating job status
    path('get-job/', GetOneJobView.as_view(), name='get-job'), # URL pattern for retrieving a single job
    path('get-all-jobs/', GetAllJobsView.as_view(), name='get-all-jobs'), # URL pattern for retrieving all jobs
    path('get-job-history/', GetJobHistoryView.as_view(), name='get-job-history'), # URL pattern for retrieving job history
    path('get-completed-jobs/', GetCompletedJobsView.as_view(), name='get-completed-jobs'), # URL pattern for retrieving completed jobs
    path('delete-job/', DeleteJobsView.as_view(), name='delete-job') # URL pattern for deleting a job
]
