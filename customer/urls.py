from django.urls import path,include
from . import views
from accounts import views as AccountViews

urlpatterns=[
    path('',AccountViews.custDashboard,name="customer"),
    path('profile/',views.cprofile,name='cprofile'),
    #my orders
    path('my_orders/',views.my_orders,name='customer_my_order'),
    #order _Details view
    path('order_detail/<int:order_number>',views.order_detail,name='order_detail')
]