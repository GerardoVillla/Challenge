from django.urls import path, include
from .views import UrlView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'url', UrlView, 'url')
urlpatterns = [
    path('api/', include(router.urls))
]


