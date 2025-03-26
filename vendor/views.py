from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse('<h1>This is just a joke now!</h1>')


def vprofile(request):
    return render(request,'vendor/vprofile.html')



# context preprocessor
# it is a function takes one argument that is request and returns a request context dictionary
