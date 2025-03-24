from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>This is Home Page</h1>')