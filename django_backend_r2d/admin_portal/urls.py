from django.urls import path
from .admin import staff_admin_site

urlpatterns = [
    path('manage', staff_admin_site.urls),
]
