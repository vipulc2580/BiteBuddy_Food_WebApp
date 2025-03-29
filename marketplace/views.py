from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from vendor.models import Vendor
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from .models import Cart 
from .context_processors import get_cart_counter,get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.
def marketplace(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active=True)
    context={
        'vendors':vendors
    }
    return render(request,'marketplace/listings.html',context)

def vendor_detail(request,vendor_slug):
    vendor=get_object_or_404(Vendor,vendor_slug=vendor_slug)
    # print(vendor)
    #reverse lookup basically fetching the category with fooditems and also category which has fooditems is_available is set to True
    categories=Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('fooditems',
         queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
    else:
        cart_items=None
    context={
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request,'marketplace/vendor_detail.html',context)

@login_required(login_url='login')
@never_cache
def add_to_cart(request,food_id=None):
    # print(food_id)
    if request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            try:
                fooditem = FoodItem.objects.get(id=food_id)

                # Get the cart item or create a new one
                chkCart, created = Cart.objects.get_or_create(user=request.user, fooditem=fooditem, defaults={'quantity': 1})

                if not created:  # If item exists, increment quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    message = 'Increased the cart quantity'
                else:
                    message = 'Added food item to the cart'

                # Fetch updated cart items
                qty= 1 if created else chkCart.quantity
                return JsonResponse({
                    'status': 'Success',
                    'message': message,
                    'cart_counter': get_cart_counter(request),
                    'qty': qty,
                    'cart_amount':get_cart_amounts(request),
                })

            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This food item does not exist'})

        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})

    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please Login to continue'})

@login_required(login_url='login')
def decrease_cart(request,food_id=None):
    if request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            try:
                fooditem = FoodItem.objects.get(id=food_id)

                # Get the cart item or create a new one
                try:
                    chkCart=Cart.objects.get(user=request.user,fooditem=fooditem)
                    if chkCart.quantity>1:
                        chkCart.quantity-=1
                        qty=chkCart.quantity
                        chkCart.save()
                        message='Decreased the food item quantity'
                    else:
                        chkCart.delete()
                        qty=0
                        message='Removed fooditem from cart'
                    return JsonResponse({
                        'status': 'Success',
                        'message': message,
                        'cart_counter': get_cart_counter(request),
                        'cart_amount':get_cart_amounts(request),
                        'qty': qty,
                    })
                except Cart.DoesNotExist:
                    return JsonResponse({'status': 'Failed', 'message': 'Item not in cart'})
            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This food item does not exist'})

        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})

    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please Login to continue'})

@login_required(login_url='login')
@never_cache
def cart(request):
    cart_items=None
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    context={
        'cart_items':cart_items
    }
    print(cart_items)
    return render(request,'marketplace/cart.html',context)

@login_required(login_url='login')
def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            try:
                chkCart = Cart.objects.filter(user=request.user, id=cart_id)

                if chkCart.exists():  # Check if cart item exists
                    chkCart.delete()
                    status = 'Success'
                    message = 'Cart Item has been deleted!'
                else:
                    status='Failed'
                    message='Cart Item does not exist in Cart'
                return JsonResponse({
                    'status': status,
                    'message': message,
                    'cart_counter': get_cart_counter(request),
                    'cart_amount':get_cart_amounts(request),
                })

            except Cart.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist in Cart'})

        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please Login!'})
