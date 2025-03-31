from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from .forms import VendorForm,OpeningHourForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor,OpeningHour
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category,FoodItem
from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify
from django.db import IntegrityError

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
    fooditems=FoodItem.objects.filter(category=category,vendor=vendor).order_by('created_at')
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
            category.save()
            category.slug=slugify(category_name)+'-'+str(category.id)
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

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,pk):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category has been deleted successfully!')
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    form=FoodItemForm()
    if request.method=='POST':
        form=FoodItemForm(request.POST,request.FILES)
        if form.is_valid():
            food_title=form.cleaned_data['food_title']
            foodItem=form.save(commit=False)
            foodItem.slug=slugify(food_title)
            foodItem.vendor=get_vendor(request)
            foodItem.save()
            messages.success(request,'Food Item has been added successfully!')
            return redirect('fooditems_by_category',pk=foodItem.category.id)
    # modify the form 
    form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
    context={
        'form':form
    }
    return render(request,'vendor/add_food.html',context)

def edit_food(request,pk):
    foodItem=get_object_or_404(FoodItem,pk=pk)
    form=FoodItemForm(instance=foodItem)
    if request.method=='POST':
        form=FoodItemForm(request.POST,request.FILES,instance=foodItem)
        if form.is_valid():
            food_title=form.cleaned_data['food_title']
            foodItem=form.save(commit=False)
            foodItem.slug=slugify(food_title)
            foodItem.vendor=get_vendor(request)
            foodItem.save()
            messages.success(request,'Food Item has been updated successfully!')
            return redirect('fooditems_by_category',pk=foodItem.category.id)
    form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
    context={
        'form':form,
        'food':foodItem,
    }
    return render(request,'vendor/edit_food.html',context)

    
def delete_food(request,pk):
    foodItem=get_object_or_404(FoodItem,pk=pk)
    foodItem.delete()
    messages.success(request,'Food Item has been deleted successfully!')
    return redirect('fooditems_by_category',pk=foodItem.category.id)


def opening_hours(request):
    vendor_opening_hours=OpeningHour.objects.filter(vendor=get_vendor(request))
    form=OpeningHourForm()
    context={
        'form':form,
        'opening_hours':vendor_opening_hours,
    }
    return render(request,'vendor/opening_hours.html',context)


def add_opening_hours(request):
    if request.user.is_authenticated:
        # handle the data and save them inside the database
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" and request.method=='POST':
            day=request.POST.get('day')
            from_hour=request.POST.get('from_hour')
            to_hour=request.POST.get('to_hour')
            is_closed=request.POST.get('is_closed')
            try:
                hour=OpeningHour.objects.create(vendor=get_vendor(request),day=day,from_hour=from_hour,to_hour=to_hour,is_closed=is_closed)
                if hour:
                    day=OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response={'status':'Success','id':hour.id,'day':day.get_day_display(),'is_closed':'Closed','message':'Opening Hour Added Successfully!'}
                    else:
                        response={'status':'Success','id':hour.id,'day':day.get_day_display(),'from_hour':hour.from_hour,'to_hour':hour.to_hour,'is_closed':'Not Closed','message':'Opening Hour Added Successfully!'}
            except IntegrityError as e:
                print(get_vendor(request),from_hour,to_hour,is_closed)
                response={'status':'Failed','message':from_hour+'-'+to_hour+' already exists for this day!'}
            return JsonResponse(response)
        else:
            return JsonResponse({'status':'Failed','message':'Invalid Request'})
    return JsonResponse({'status':'Failed','message':'Please Login!'})

def remove_opening_hours(request,pk=None):
    if request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            hour=OpeningHour.objects.get(pk=pk)
            if hour:
                hour.delete()
                response={
                    'status':'Success',
                    'message':'Opening Hour Deleted Successfully!',
                    'id':pk
                }
            else:
                response={
                    'status':'Failed',
                    'message':'Internal Error occured!'
                }
            return JsonResponse(response)
        else:
            return JsonResponse({
                'status':'Failed',
                'message':'Invalid Request',
            })
    else:
        return JsonResponse({'status':'Failed','message':'Login Required!'})