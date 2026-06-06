"""
URL configuration for campaign_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.dashboard_view, name='dashboard'),
    path('templates/', views.template_list, name='template_list'),
    path('templates/new/', views.template_create, name='template_create'),
    path('contacts/', views.contact_list_view, name='contact_lists'),
    path('contacts/upload/', views.contact_upload, name='contact_upload'),
    path('campaigns/new/', views.campaign_create, name='campaign_create'),
]
