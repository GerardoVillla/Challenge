from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Url
from .serializer import UrlSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import get_authorization_header
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
from django.core.paginator import Paginator

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

@api_view(['DELETE'])
def delete_public_url(request):
    original_url = request.data['original_url']
    url = Url.objects.filter(original_url=original_url, is_public=True).first()
    url.delete()
    return Response({'original_url' : original_url, 'short_url' : ""}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
def update_public_url(request):
    original_url = request.data['original_url']
    new_url = request.data['new_url']
    url = Url.objects.filter(original_url=original_url, is_public=True).first()
    url.original_url = new_url
    url.save()
    return Response({'original_url' : new_url, 'short_url': url.short_url}, status=status.HTTP_200_OK)

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

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_private_url(request):
    original_url = request.data['original_url']
    url = Url.objects.filter(original_url=original_url, is_public=False, user=request.user).first()
    url.delete()
    return Response({'original_url' : original_url, 'short_url' : ""}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_private_url(request):
    original_url = request.data['original_url']
    new_url = request.data['new_url']
    url = Url.objects.filter(original_url=original_url, is_public=False, user=request.user).first()
    url.original_url = new_url
    url.save()
    return Response({'original_url' : new_url, 'short_url': url.short_url}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_massive_urls(request):
    urls = request.data.get('urls', [])
    if not urls:
        return Response({'error': 'No se proporcionaron URLs'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not isinstance(urls, list):
        return Response({'error': 'El campo "urls" debe ser una lista.'}, status=status.HTTP_400_BAD_REQUEST)
    
    host = request.get_host()
    response = []

    for url_data in urls:
        original_url = url_data.get('original_url')
        if not original_url:
            continue  # Ignora objetos que no tengan 'original_url'
        
        if is_unique_public_url(original_url):
            short_url = get_unique_short_url(original_url)
            response.append({'original_url': original_url, 'short_url': short_url})
        else:
            short_url = shorten_url(host)
            url_obj = Url(original_url=original_url, short_url=short_url)
            url_obj.save()
            response.append({'original_url': original_url, 'short_url': short_url})
    
    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_massive_urls(request, page_number=1):
    urls = Url.objects.all()
    page_size = 20
    paginator = Paginator(urls, page_size)
    page = paginator.get_page(page_number)
    serializer = UrlSerializer(page, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def redirect_to_url(request, short_code):
    #short_code = request.build_absolute_uri()  
    short_code = request.get_host() + '/' + short_code
    url = get_object_or_404(Url, short_url=short_code)
    auth_header = get_authorization_header(request).decode('utf-8')  # Obtener el encabezado de autorización
    if url.is_public == False and auth_header and auth_header.startswith('Token'):
        token = auth_header.split(' ')[1]
        if token != url.user.auth_token.key:
            return Response({'error': 'You do not have permission to access this url'}, status=status.HTTP_403_FORBIDDEN)
    url.clicks += 1
    url.save()
    return redirect(url.original_url)