from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('create/', views.create_public_url),
    path('create-auth/', views.create_private_url),
]


