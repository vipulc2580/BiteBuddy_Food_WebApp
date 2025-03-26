from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from django.contrib import messages,auth
from .utils import detectUser,send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor


#restrict vendor from accessing customer page
def check_role_vendor(user):
    # print(f"User Role: {user.role}")  # Debugging line
    if user.role==1:
        return True 
    else:
        raise PermissionDenied

def check_role_customer(user):
    print(f"User Role: {user.role}")  # Debugging line
    if user.role==2:
        return True 
    else:
        raise PermissionDenied

# restrict customer from accessing vendor page

def register_user(request):
    form=None
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect('myAccount')
    elif request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            user=form.save(commit=False)
            user.role=User.CUSTOMER
            user.set_password(password)
            user.save()
            #create user using create_user method
            # first_name=form.cleaned_data['first_name']
            # last_name=form.cleaned_data['last_name']
            # username=form.cleaned_data['username']
            # email=form.cleaned_data['email']
            # password=form.cleaned_data['password']
            # user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            # user.role=User.CUSTOMER
            # user.save()


            # send verification email 
            mail_subject='Please activate your account'
            htmlfile='account_verification.html'
            send_verification_email(request,user,mail_subject,htmlfile)
            messages.success(request,"You're account has been registered successfully!")
            # return HttpResponse('<h1>User has been Registered</h1>')
            return redirect('register_user')
    else:
        form=UserForm()
    context={
        'form':form
    }
    return render(request,'accounts/registerUser.html',context)

def register_restaurant(request):
    form=UserForm()
    v_form=VendorForm()
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect('myAccount')
    elif request.method=='POST':
        # print('post request recieved')
        form=UserForm(request.POST)
        v_form=VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.role=User.VENDOR
            user.save()
            vendor=v_form.save(commit=False)
            vendor.user=user
            vendor.user_profile=UserProfile.objects.get(user=user)
            vendor.save()

            # sending the verification email
            mail_subject='Please activate your account'
            htmlfile='account_verification.html'
            send_verification_email(request,user,mail_subject,htmlfile)

            messages.success(request,'Your vendor account has been registered successfully,Please wait for approval')
            # print('Vendor successfully saved')
            return redirect('register_vendor')
        else:
            print('Invalid form')
            print(form.errors)
    context={
        'form':form,
        'v_form':v_form
    }
    return render(request,'accounts/registerVendor.html',context)
    

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect('myAccount')
    elif request.method=='POST':
        print('request recieved')
        # print(request.POST)
        email=request.POST['email']
        password=request.POST['password']
        # print(email,password)
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You've successfully logged In!")
            return redirect('myAccount')
        else:
            messages.error(request,'Invalid Login credentials')
            return redirect('login')

    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request,"You're logged out")
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    if request.user.role==2:
        messages.warning(request,'You are logged in as Customer')
        return redirect('myAccount')
    return render(request,'accounts/vendorDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request,'accounts/custDashboard.html')

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True  
        user.save()
        messages.success(request,"Congratulation! Your account is activated.")
        return redirect('myAccount')
    else:
        messages.error(request,'Invalid activation link')
    # activate the user by setting the is-active status to true
    return redirect('myAccount')



def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)
            
            # send reset password email
            mail_subject='Reset Your Password'
            htmlfile='reset_password_email.html'
            send_verification_email(request=request,user=user,mail_subject=mail_subject,htmlfile=htmlfile)

            messages.success(request,'Password reset link has been sent your email address.')
            return redirect('login')
        else:
            messages.error(request,'Account does not exist.')
            return redirect('forgot_password')
    return render(request,'accounts/forgot_password.html')


def reset_password_validate(request,uidb64,token):
    # validating the user by decoding the user token
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid 
        messages.info(request,'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired!')
    # activate the user by setting the is-active status to true
    return redirect('myAccount')
    
def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            pk=request.session.get('uid')
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True 
            user.save()
            messages.success(request,'Password has been reset successfully!')
            return redirect('login')
        else:
            messages.error(request,'Password do not match')
            return redirect('reset_password')
    return render(request,'accounts/reset_password.html')

def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)