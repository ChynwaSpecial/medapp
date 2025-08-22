from django.shortcuts import render
from .models import Service

def home(request):
    services = Service.objects.all()
    return render(request, 'core/home.html', {'services': services})
def about(request):
    return render(request, 'core/about.html')
def contact(request):
    return render(request, 'core/contact.html')
def services(request):
    return render(request, 'core/services.html')
def help(request):
    return render(request, 'core/help.html')





