from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),


     # path('profile', views.profile, name='profile'),
     path('editprofile', views.editprofile, name="editprofile"),
     path('getupdatedprofile', views.getupdatedprofile, name="getupdatedprofile"),
     path('vehicles', views.vehicles, name='vehicles'),
     path('cart', views.cart, name='cart'),
     path('view_bookings', views.view_bookings, name='view_bookings'),
     path('feedback', views.feedback, name='feedback'),
     path('viewmorevehicledetails/<int:vmoreid>/', views.viewmorevehicledetails, name='viewmorevehicledetails'),
     path('addtocart/<int:vhid>/', views.addtocart, name='addtocart'),
     # path('book/<int:vhid>/', views.book, name='book'),
     path('vbook1/<int:bvhid>/', views.vbook1, name="vbook1"),
     path('vbook2/<int:bvhid2>/', views.vbook2, name="vbook2"),

     path('paymenthandler', views.paymenthandler, name="paymenthandler"),
     path('paymenthandler2', views.paymenthandler2, name="paymenthandler2"),
     path('home', views.home, name="home"),
     path('home2', views.home2, name="home2"),
     # path('payment', views.payment, name="payment"),
     path('deletefromcart/<int:cid>/', views.deletefromcart, name="deletefromcart"),







     # path('viewvehicles', views.viewvehicles, name='viewvehicles'),
     # path('selectedvehicle', views.selectedvehicle, name='selectedvehicle'),

]