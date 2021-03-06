"""shoes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path

from core.views import (ApiUsersView, ApiFeedView, IndexView, ApiSearchView,
                        ApiCustomTagsView, ApiExcludeView, ApiLocationsView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', ApiUsersView.as_view(), name='api_users'),
    path('api/feed/', ApiFeedView.as_view(), name='api_feed'),
    path('api/search/', ApiSearchView.as_view(), name='api_feed'),
    path('api/custom_tags/<str:media_id>', ApiCustomTagsView.as_view(),
         name='api_custom_tags'),
    path('api/exclude/<str:media_id>', ApiExcludeView.as_view(),
         name='api_exclude'),
    path('api/locations/', ApiLocationsView.as_view(), name='locations'),
    path('', IndexView.as_view(), name='index'),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='core/login.html'),
        name='login'
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(next_page='index'),
        name='logout'
    ),
]
