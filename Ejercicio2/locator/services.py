import random
import string
from .models import Url


CHARS = string.ascii_letters + string.digits

def shorten_url(host: str) -> str:
    code = ''.join(random.choice(CHARS) for i in range(6))
    return host + '/' + code 	
  		
def is_unique_public_url(original_url: str) -> bool:
    return Url.objects.filter(original_url=original_url, is_public=True).exists()

def get_unique_short_url(original_url: str) -> str:
	return Url.objects.filter(original_url=original_url, is_public=True).first().short_url