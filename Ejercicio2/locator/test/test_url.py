import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_create_public_url(api_client):
    url = reverse('urls-list')
    data = {'original_url': 'https://google.com',}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'short_url' in response.data
    code = response.data['short_url'].split('/')[-1]
    url = reverse('redirect', kwargs={'short_code':code})
    redirect_response = api_client.get(url, format='json')
    assert redirect_response.status_code == status.HTTP_302_FOUND
    assert redirect_response.url == "https://google.com"
    
@pytest.mark.django_db
def test_create_private_url(api_client, django_user_model):
    api_client.login(username='testuser', password='testpass')
    url = reverse('urls-list')
    data = {'original_url': 'https://google.com',} 
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'short_url' in response.data

@pytest.mark.django_db
def test_create_massive_urls(api_client):
    url = reverse('urls-list')
    data = {
        'urls': [
            {'original_url': 'https://example1.com',},
            {'original_url': 'https://example2.com',} 
        ]
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.data) == 1
