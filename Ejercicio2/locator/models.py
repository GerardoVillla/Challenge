from django.db import models
from authentication.models import CustomUser

# Create your models here.


class Url(models.Model): 
    original_url = models.URLField(max_length=5000)
    short_url = models.CharField(max_length=5000, unique=True)
    is_public = models.BooleanField(default=True)
    clicks = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']
