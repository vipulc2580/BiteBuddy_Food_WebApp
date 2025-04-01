from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm,UserInfoForm
from accounts.models import UserProfile,User
from django.contrib import messages
from orders.models import Order,OrderedFood
import json
# Create your views here.
@login_required
def cprofile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    if request.method=='POST':
        profile_form=UserProfileForm(request.POST,request.FILES,instance=profile)
        user_form=UserInfoForm(request.POST,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Profile Updated!')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    profile_form=UserProfileForm(instance=profile)
    user_form=UserInfoForm(instance=request.user)
    context={
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }
    return render(request,'customers/cprofile.html',context)

@login_required
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders':orders,
    }
    return render(request,'customers/my_orders.html',context)

@login_required
def order_detail(request,order_number):
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_food=OrderedFood.objects.filter(order=order)
        subtotal=0
        for item in ordered_food:
            subtotal+=(item.price*item.quantity)
        # print(subtotal)
        tax_data=json.loads(order.tax_data)
        # print(tax_data)
        context={
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':subtotal,
            'tax_data':tax_data,
        }
        return render(request,'customers/order_detail.html',context)
    except:
        messages.error(request,'Something went wrong!!')
        return redirect('customer')