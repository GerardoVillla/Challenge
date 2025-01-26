from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Url
from .serializer import UrlSerializer
from rest_framework.views import APIView

# Create your views here.

class UrlView(viewsets.ModelViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
    