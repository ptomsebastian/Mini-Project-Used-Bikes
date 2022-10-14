
from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.apps import apps
User = apps.get_model('labadmin', 'User')
Customer = apps.get_model('labadmin', 'Customer')
Brand = apps.get_model('labadmin', 'Brand')
Vehiclename = apps.get_model('labadmin', 'Vehiclename')
Vehicle = apps.get_model('labadmin', 'Vehicle')
Info = apps.get_model('labadmin', 'Info')
Cart = apps.get_model('labadmin', 'Cart')
Booking = apps.get_model('labadmin', 'Booking')
Feedback = apps.get_model('labadmin', 'Feedback')


def index(request):
    print("hai")
    return render(request, '/labadmin/templates/login.html')

def profile(request):
    return HttpResponse("success")

# def vehicles(request):
#     return HttpResponse("success")

def vehicles(request):
    brnd = Brand.objects.all().order_by('name').values()
    vehicles = Vehicle.objects.all().values()
    vname = Vehiclename.objects.all().values()
    print(vehicles)
    context = {'brnd': brnd, 'vehicles': vehicles, 'vname': vname}
    return render(request, 'customer/1viewvehicles.html', context)


def cart(request):
    return render(request, 'customer/3cart.html')

def view_bookings(request):
    return render(request, 'customer/4bookings.html')

def feedback(request):
    return HttpResponse("success")


# def viewvehicles(request):
#         brnd = Brand.objects.all().order_by('name').values()
#         vehicles = Vehicle.objects.all().values()
#         vname = Vehiclename.objects.all().values()
#         print(vehicles)
#         context = {'brnd': brnd, 'vehicles': vehicles, 'vname': vname}
#         return render(request, 'labadmin/6vehicle manage.html', context)