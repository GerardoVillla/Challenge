from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('create/', views.create_public_url),
    path('delete/', views.delete_public_url),
    path('update/', views.update_public_url),
    path('create-massive/', views.create_massive_urls),
    path('urls/<int:page_number>', views.get_massive_urls),
    path('create-auth/', views.create_private_url),
    
]


