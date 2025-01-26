from django.db import models
from django.db.models import Model

# Create your models here.


class url(models.Model): 
    originalUrl = models.CharField(max_length=5000, required=True)
    isPublic = models.BooleanField(default=True)
    shortUrl = models.CharField(max_length=5000, required=True)
    clicks = models.IntegerField(default=0)
    idUser = models.ForeignKey('User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']
