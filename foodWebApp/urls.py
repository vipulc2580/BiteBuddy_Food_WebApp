"""
URL configuration for foodWebApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403
from accounts.views import custom_403_view
from marketplace import views as marketplaceviews
handler403 = custom_403_view

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',views.home,name='home'),
    path('',include('accounts.urls')),
    path('marketplace/',include('marketplace.urls')),
    #Cart
    path('cart/',marketplaceviews.cart,name='cart'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
