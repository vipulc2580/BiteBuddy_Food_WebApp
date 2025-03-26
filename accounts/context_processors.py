from vendor.models import Vendor

def get_vendor(request):
    try:
        vendor=Vendor.objects.get(user=request.user)
        return dict(vendor=vendor)
    except:
        return dict(vendor=None)