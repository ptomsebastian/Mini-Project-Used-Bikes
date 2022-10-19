from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),


     path('profile', views.profile, name='profile'),
     path('vehicles', views.vehicles, name='vehicles'),
     path('cart', views.cart, name='cart'),
     path('view_bookings', views.view_bookings, name='view_bookings'),
     path('feedback', views.feedback, name='feedback'),
     path('viewmorevehicledetails/<int:vmoreid>/', views.viewmorevehicledetails, name='viewmorevehicledetails'),
     path('addtocart/<int:vhid>/', views.addtocart, name='addtocart'),
     # path('book/<int:vhid>/', views.book, name='book'),

     path('paymenthandler', views.paymenthandler, name="paymenthandler"),
     path('home', views.home, name="home"),
     path('payment', views.payment, name="payment"),
     path('deletefromcart/<int:cid>/', views.deletefromcart, name="deletefromcart"),







     # path('viewvehicles', views.viewvehicles, name='viewvehicles'),
     # path('selectedvehicle', views.selectedvehicle, name='selectedvehicle'),

]