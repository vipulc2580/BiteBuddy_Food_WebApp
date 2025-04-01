from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from vendor.models import Vendor
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import paypalrestsdk
import requests
from marketplace.context_processors import get_cart_amounts
from orders.views import payments,order_complete

PAYPAL_CLIENT_ID = settings.PAYPAL_CLIENT_ID
PAYPAL_SECRET =settings.PAYPAL_SECRET_KEY
PAYPAL_API_URL = "https://api-m.sandbox.paypal.com"


def home(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active=True)
    # print(vendors)
    context={
        'vendors':vendors
    }
    return render(request,'index.html',context)




@csrf_exempt
def create_order(request):
    auth = (PAYPAL_CLIENT_ID, PAYPAL_SECRET)
    headers = {"Content-Type": "application/json"}

    grand_total=get_cart_amounts(request)['grand_total']
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value":str(grand_total),
            }
        }]
    }

    response = requests.post(
        f"{PAYPAL_API_URL}/v2/checkout/orders",
        json=order_data,
        auth=auth,
        headers=headers
    )

    if response.status_code == 201:
        return JsonResponse(response.json())  # Return the valid order ID
    else:
        return JsonResponse(response.json(), status=400)

@csrf_exempt

def capture_order(request, order_id,order_number):
    """Captures an approved PayPal order"""

    auth = (PAYPAL_CLIENT_ID, PAYPAL_SECRET)
    headers = {"Content-Type": "application/json"}

    capture_url = f"{PAYPAL_API_URL}/v2/checkout/orders/{order_id}/capture"

    response = requests.post(capture_url, auth=auth, headers=headers)

    if response.status_code == 201 or response.status_code == 200:

        response_obj = response.json()  # No need to use json.load()
        transaction = response_obj['purchase_units'][0]['payments']['captures'][0]
        # print(transaction)
        transaction_id=transaction['id']
        status=transaction['status']
        payment_method='PayPal'
        # print(transaction_id,status,payment_method,order_number)
        # make payment entry in database
        return payments(request,transaction_id,status,payment_method,order_number)
         # Success! Return capture response

    return JsonResponse(response.json(), status=response.status_code)  # Handle errors