from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.myAccount),
    path('registerUser/',views.register_user,name='register_user'),
    path('registerVendor/',views.register_restaurant,name='register_vendor'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),

    # directing user to appropriate dashboard
    path('custDashboard/',views.custDashboard,name='custDashboard'),
    path('myAccount/',views.myAccount,name='myAccount'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),

    #related to activating the account 
    path('activate/<uidb64>/<token>',views.activate,name='activate'),

    # related to password resetting
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/',views.reset_password_validate,name='reset_password_validate'),
    path('rest_password/',views.reset_password,name='reset_password'),
    path('change_password/',views.change_password,name='change_password'),

    # vendor profile
    path('vendor/',include('vendor.urls')),

    # customer profile
    path('customer/',include('customer.urls')),
]
