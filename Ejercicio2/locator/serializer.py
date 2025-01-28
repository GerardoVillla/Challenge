from rest_framework import serializers
from .models import Url

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = "__all__"
        read_only_fields = ['short_url', 'clicks', 'user', 'created', 'is_public']