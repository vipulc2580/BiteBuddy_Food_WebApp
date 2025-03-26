from django.http import HttpResponse
from django.shortcuts import render,redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('myAccount')
    return render(request,'index.html')
