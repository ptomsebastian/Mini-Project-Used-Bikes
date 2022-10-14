from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),


     path('profile', views.profile, name='profile'),
     path('vehicles', views.vehicles, name='vehicles'),
     path('cart', views.cart, name='cart'),
     path('view_bookings', views.view_bookings, name='view_bookings'),
     path('feedback', views.feedback, name='feedback'),


     # path('viewvehicles', views.viewvehicles, name='viewvehicles'),
     # path('selectedvehicle', views.selectedvehicle, name='selectedvehicle'),

]