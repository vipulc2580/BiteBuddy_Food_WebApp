from .models import Cart,Tax
from menu.models import FoodItem

def get_cart_counter(request):
    cart_count=0
    if request.user.is_authenticated:
        try:
            cart_items=Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count+=(cart_item.quantity)
            else:
                cart_count=0
        except:
            cart_count=0
    return dict(cart_count=cart_count)

def get_cart_amounts(request):
    subtotal=0
    taxes={}
    # tax dict {'tax_type':{'tax_percentage':'tax_amount'}}
    grand_total=0
    total_tax=0
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem=FoodItem.objects.get(id=item.fooditem.id)
            subtotal+=(fooditem.price*item.quantity)
        get_taxes=Tax.objects.filter(is_active=True)
        # print(list(get_taxes))
        for tax in get_taxes:
            # print(tax.tax_type,tax.tax_percentage)
            tax_type=tax.tax_type
            tax_percentage=tax.tax_percentage
            tax_amount=round((subtotal*(tax_percentage/100)),2)
            total_tax+=tax_amount
            # print(tax_type,tax_percentage,tax_amount)
            tax_dict={str(tax_percentage):str(tax_amount)}
            taxes.update({tax_type:tax_dict})
        grand_total=subtotal+total_tax

    return dict(subtotal=subtotal,grand_total=grand_total,taxes=taxes)