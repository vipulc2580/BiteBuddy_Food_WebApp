from django.db import models
from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor
import json
request_object=None
class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PayPal', 'PayPal'),
        ('RazorPay', 'RazorPay'), # Only for Indian Students.
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=20)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    vendors=models.ManyToManyField(Vendor,blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text = "Data format: {'tax_type':{'tax_percentage':'tax_amount'}}",null=True)
    total_data=models.JSONField(blank=True,null=True)
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def order_placed_to(self):
        return ','.join([i.vendor_name for i in self.vendors.all()])
    
    def get_total_by_vendor(self):
        vendor=Vendor.objects.get(user=request_object.user)
        subtotal=0
        tax_data={}
        grand_total=0
        total_tax=0
        if self.total_data:
            vendor_cart_details=json.loads(self.total_data).get(str(vendor.id))
            for key,val in vendor_cart_details.items():
                subtotal=float(key)
                tax_data=val 
            # print(subtotal,tax_data)
            
            for taxes in tax_data.values():
                for tax_amount in taxes.values():
                    total_tax += float(tax_amount) 
        # print(total_tax)
        grand_total=total_tax+subtotal
        return {'subtotal':subtotal,'grand_total':grand_total,'tax_data':tax_data}

    def __str__(self):
        return self.order_number

# total_data in vendor model
# Vendor Specific json which holds Vendor level detail
# Sub total for vendor products
# Tax .Tax Type,Tax Percentage,Tax amount
# Grand total for of current order for current vendor
# {'vendor id':{'subtotal':{'tax_type':{'tax_percentage':'tax_amount'}}}}

class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_title