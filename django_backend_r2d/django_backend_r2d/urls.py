"""
URL configuration for django_backend_r2d project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include

"""
When onboarding new applications, include the api/app-name-abbreviation
"""
urlpatterns = [ 
    path('admin/', admin.site.urls), # url for the admin portal
    path('api/accounts/', include('accounts.urls')), # URL for the accounts app
    path('api/auth/', include('authentication.urls')), # URL for the authentication app
    path('staff-administration/', include('admin_portal.urls')), # URL for the staff admin portal
    path('api/jobs/', include('jobs.urls')) # URL for the jobs app
]
