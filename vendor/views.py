from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category,FoodItem
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify

# Create your views here.

def get_vendor(request):
    vendor=Vendor.objects.get(user=request.user)
    return vendor
def home(request):
    return HttpResponse('<h1>This is just a joke now!</h1>')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    vendor=get_object_or_404(Vendor,user=request.user)
    if request.method=='POST':
        profile_form=UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form=VendorForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            # print(profile_form)
            # print(vendor_form)
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Restaurant Details has been updated!')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form=UserProfileForm(instance=profile)
        vendor_form=VendorForm(instance=vendor)
    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request,'vendor/vprofile.html',context)



# context preprocessor
# it is a function takes one argument that is request and returns a request context dictionary



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor=get_vendor(request)
    categories=Category.objects.filter(vendor=vendor).order_by('created_at')
    context={
        'categories':categories
    }
    return render(request,'vendor/menu_builder.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    vendor=get_vendor(request)
    category=get_object_or_404(Category,pk=pk)
    fooditems=FoodItem.objects.filter(category=category,vendor=vendor)
    # print(fooditems)
    context={
        'fooditems':fooditems,
        'category':category,
    }
    return render(request,'vendor/fooditems_by_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    form=CategoryForm()
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.slug=slugify(category_name)
            category.save()
            messages.success(request,'New Category added successfully!')
            return redirect('menu_builder')
    context={
        'form':form
    }
    return render(request,'vendor/add_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    form=CategoryForm(instance=category)
    if request.method=='POST':
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.slug=slugify(category_name)
            category.save()
            messages.success(request,'Category updated Successfully!')
            return redirect('menu_builder')
    context={
        'form':form,
        'cat':category,
    }
    return render(request,'vendor/edit_category.html',context)

def delete_category(request,pk):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category has been deleted successfully!')
    return redirect('menu_builder')