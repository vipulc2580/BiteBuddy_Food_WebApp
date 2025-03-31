from django.http import HttpResponse
from django.shortcuts import render,redirect
from vendor.models import Vendor
def home(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active=True)
    # print(vendors)
    context={
        'vendors':vendors
    }
    return render(request,'index.html',context)
