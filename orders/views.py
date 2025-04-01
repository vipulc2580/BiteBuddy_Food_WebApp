from django.shortcuts import render,redirect
from django.http import JsonResponse
from marketplace.models import Cart 
from orders.forms import OrderForm
from django.contrib import messages
from marketplace.context_processors import get_cart_amounts
from .models import Order,Payment,OrderedFood
import json
from .utils import generate_order_number
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def place_order(request):
    cart_items=Cart.objects.filter(user=request.user)
    cart_count=cart_items.count()
    if cart_count<=0:
        messages.error(request,'Cart is Empty,Fill the Cart')
        return redirect('marketplace')
    subtotal=get_cart_amounts(request)['subtotal']
    total_tax=get_cart_amounts(request)['total_tax']
    grand_total=get_cart_amounts(request)['grand_total']
    taxes=get_cart_amounts(request)['taxes']
    # print(subtotal,total_tax,grand_total,taxes)
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            order=Order()
            order.first_name=form.cleaned_data['first_name']
            order.last_name=form.cleaned_data['last_name']
            order.phone=form.cleaned_data['phone']
            order.email=form.cleaned_data['email']
            order.address=form.cleaned_data['address']
            order.country=form.cleaned_data['country']
            order.state=form.cleaned_data['state']
            order.city=form.cleaned_data['city']
            order.pin_code=form.cleaned_data['pin_code']
            order.user=request.user
            order.total=grand_total
            order.total_tax=total_tax
            order.tax_data=json.dumps(taxes)
            order.payment_method=request.POST['payment_method']
            # print(request.POST['payment_method'])
            order.save()
            order.order_number=generate_order_number(order.id)
            order.save()
            context={
                'order':order,
                'cart_items':cart_items,
            }
            return render(request,'orders/place_order.html',context)
        else:
            print(form.errors)
    return render(request,'orders/place_order.html')


def payments(request,transaction_id,status,payment_method,order_number):
    order=Order.objects.get(user=request.user,order_number=order_number)
    # Store payment details in payment model
    payment=Payment(transaction_id=transaction_id,payment_method=payment_method,status=status,user=request.user,amount=order.total)
    payment.save()
    # update the order model status payment is done
    order.payment=payment
    order.is_ordered=True 
    order.save()
    #Move the cart items to Ordered Food Model
    cart_items=Cart.objects.filter(user=request.user)
    for item in cart_items:
        ordered_food=OrderedFood()
        ordered_food.order=order
        ordered_food.payment=payment
        ordered_food.fooditem=item.fooditem
        ordered_food.quantity=item.quantity
        ordered_food.price=item.fooditem.price
        ordered_food.amount=(item.fooditem.price*item.quantity)
        ordered_food.user=request.user
        ordered_food.save()
    #Send order confirmation email to the customer
    mail_subject='Thank you for ordering with us!'
    mail_template='orders/order_confirmation_email.html'
    context={
        'user':request.user,
        'order':order,
        'to_email':order.email,
    }
    send_notification(mail_subject,mail_template,context)

    # send order receive email to vendor
    mail_subject='You have recieved a new order!'
    mail_template='orders/new_order_received.html'
    to_emails=list({item.fooditem.vendor.user.email for item in cart_items})
    context={
        'order':order,
        'to_email':to_emails,
    }
    send_notification(mail_subject,mail_template,context)
    # clear the cart once the payment is successful
    # cart_items.delete()
    # return the response ( status success or failure)
    response={
        'status':200,
        'order_number':order.order_number,
        'transaction_id':order.payment.transaction_id,
        'message':'Payment Done',
    }
    return JsonResponse(response)

def order_complete(request):
    order_number=request.GET.get('order_no')
    transaction_id=request.GET.get('trans_id')
    print(order_number,transaction_id)
    try:
        order=Order.objects.get(order_number=order_number,payment__transaction_id=transaction_id,is_ordered=True)
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
        return render(request,'orders/order_complete.html',context)
    except Exception as e:
        print(e)
        return redirect('home')

