from vendor.models import Vendor
from django.conf import settings
from .models import UserProfile

def get_vendor(request):
    try:
        vendor=Vendor.objects.get(user=request.user)
        return dict(vendor=vendor)
    except:
        return dict(vendor=None)

def get_google_api_key(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}

def get_user_profile(request):
    try:
        user_profile=UserProfile.objects.get(user=request.user)
    except:
        user_profile=None
    return dict(user_profile=user_profile) 
