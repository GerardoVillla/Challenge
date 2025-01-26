from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User

# Create your models here.


class Url(models.Model): 
    original_url = models.CharField(max_length=5000)
    is_public = models.BooleanField(default=True)
    short_url = models.CharField(max_length=5000)
    clicks = models.IntegerField(default=0)
    ##id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']
