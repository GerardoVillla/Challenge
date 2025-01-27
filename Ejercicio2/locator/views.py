from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Url
from .serializer import UrlSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from .models import Url
from rest_framework import status
from .services import shorten_url
from .services import is_unique_public_url
from .services import get_unique_short_url
"""
@api_view(['POST'])
def create_short_url(request):
    try:
        if request.data['original_url'] is "":
            return Response({'error': 'Original URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.data['is_public']:
            return createUrlPrivate(request)
        else:
            return createUrlPublic(request)
    except KeyError:
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        
"""

@api_view(['POST'])
def create_public_url(request):
    original_url = request.data['original_url']
    if is_unique_public_url(original_url):
        short_url = get_unique_short_url(original_url)
        return Response({'original_url' : original_url, 'short_url': short_url}, status=status.HTTP_201_CREATED)
    host = request.get_host()
    short_url = shorten_url(host)
    url = Url(original_url=original_url, short_url=short_url)
    url.save()
    return Response({'original_url' : original_url, 'short_url': short_url}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_private_url(request):
    original_url = request.data['original_url']
    host = request.get_host()
    short_url = shorten_url(host)
    url = Url(original_url=original_url, short_url=short_url, is_public=False, user=request.user)
    url.save()
    return Response({'original_url' : original_url, 'short_url': short_url}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def redirect_to_url(request, short_code):
    #short_code = request.build_absolute_uri()  
    short_code = request.get_host() + '/' + short_code
    url = get_object_or_404(Url, short_url=short_code)
    url.clicks += 1
    url.save()
    return redirect(url.original_url)