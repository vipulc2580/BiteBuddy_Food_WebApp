from django.contrib import admin
from .models import Payment,Order,OrderedFood
# Register your models here.
class OrderFoodInline(admin.TabularInline):
    model=OrderedFood
    readonly_fields=['order','payment','user','fooditem','quantity','price','amount']
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_number','name','email','phone','total','payment_method','status','order_placed_to','is_ordered']
    inlines=[OrderFoodInline]

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedFood)
