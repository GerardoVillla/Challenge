from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from .models import Url
from .serializer import UrlSerializer
from .services import shorten_url, is_unique_public_url, get_unique_short_url
from rest_framework.decorators import api_view
from django.shortcuts import redirect as django_redirect
class BaseUrlViewSet(viewsets.GenericViewSet):
    serializer_class = UrlSerializer
    lookup_field = 'original_url'
    #permission_classes = [IsPrivateURLAllowed]
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Url.objects.all()
        return Url.objects.filter(is_public=True)

    def build_response(self, url):
        return {
            'original_url': url.original_url,
            'short_url': url.short_url
        }

class UrlViewSet(BaseUrlViewSet):
    
    def _create_url(self, data, is_public):
        original_url = data['original_url']
        host = self.request.get_host()
        if is_public and is_unique_public_url(original_url):
            short_url = get_unique_short_url(original_url)
            return Response({"original_url" : original_url,"short_url" : short_url}, status=status.HTTP_200_OK)
        else:
            short_url = shorten_url(host)

        url = Url.objects.create(
            original_url=original_url,
            short_url=short_url,
            is_public=is_public,
            user=self.request.user if not is_public else None
        )
        return Response(self.build_response(url), status=status.HTTP_201_CREATED)
    
    def _delete_url(self, is_public):
        id = self.request.query_params['id']
        url = get_object_or_404(self.get_queryset(), id=id)
        url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def _update_url(self, is_public):
        id = self.request.query_params['id']
        new_url = self.request.data['new_url']
        
        url = get_object_or_404(self.get_queryset(), id=id)
        url.original_url = new_url
        url.save()
        
        return Response(self.build_response(url), status=status.HTTP_200_OK)
    
    def create(self, request):
        is_public = not self.request.user.is_authenticated
        return self._create_url(request.data, is_public)
    
    def delete(self, request):
        is_public = not self.request.user.is_authenticated
        return self._delete_url(is_public)
    
    def patch(self, request):
        is_public = not self.request.user.is_authenticated
        return self._update_url(is_public)
    
    @action(detail=False, methods=['post'])
    def create_massive(self, request):
        urls = request.data.get('urls', [])
        
        if not isinstance(urls, list):
            return Response({'error': 'Field "urls" must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = []
        for url_data in urls:
            is_public = url_data.get('is_public', False)
            if type(is_public) != bool:
                return Response({'error': 'Field is_public must be boolean'}, status=status.HTTP_400_BAD_REQUEST)
            if not is_public and not self.request.user.is_authenticated:
                return Response({'error': 'You do not have permission to create private URLs'}, status=status.HTTP_403_FORBIDDEN)
            url = self._create_url(url_data, is_public)
            response.append(url.data)
        
        return Response(response, status=status.HTTP_201_CREATED)
    @action(detail=False, methods=['get'])
    def list_massive(self, request):
        page_number = request.query_params.get('page', 1)
        paginator = Paginator(self.get_queryset(), 20)
        page = paginator.get_page(page_number)
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def redirect(request, short_code=None):
    full_short_url = request.get_host()+ "/" + short_code
    url = get_object_or_404(Url, short_url=full_short_url)
    if not request.user.is_authenticated and not url.is_public:
        return Response({'error': 'You do not have permission to access this URL'}, status=status.HTTP_403_FORBIDDEN)
    url.clicks += 1
    url.user_id = request.user.id
    url.save()
    return django_redirect(url.original_url)