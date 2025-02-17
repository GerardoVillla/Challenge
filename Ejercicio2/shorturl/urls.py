"""
URL configuration for shorturl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from authentication import views
from locator.views import redirect
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Short URL API",
        default_version='v1.0.0',
        description="API for shortening URLs",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("url/", include("locator.urls")),
    path('<str:short_code>/',redirect, name='redirect'),
    path('auth/login/', views.login),
    path('auth/register/', views.register),
    path('auth/profile/', views.profile),
    path('swagger/docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    
]
