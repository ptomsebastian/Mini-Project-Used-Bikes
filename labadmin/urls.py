from django.urls import path

from . import views
from .views import getvehicleinfo
urlpatterns = [
     path('', views.index, name='index'),
     path('login_user', views.login_user, name='login_user'),
     path('signup', views.signup, name='signup'),
     path('gk_logout', views.gk_logout, name='gk_logout'),

     path('vehicle', views.vehicle_management, name='vehicle_management'),
     path('home', views.home_page_management, name='home_page_management'),
     path('get_homeimage', views.get_homeimage, name='get_homeimage'),
     path('deletehomeimage/<int:hid>/', views.deletehomeimage, name='deletehomeimage'),
     path('book_management', views.book_management, name='book_management'),
     path('feedback', views.feedback_management, name='feedback_management'),
     path('business', views.business_report, name='business_report'),
     path('brand', views.brand_management, name='brand_management'),
     path('vehiclename', views.vehicle_name_management, name='vehicle_name_management'),
     path('logout', views.logout, name='logout'),
     path('signin', views.signin, name='signin'),
     path('register', views.register, name='register'),
     path('getregisterdata', views.getregisterdata, name='getregisterdata'),
     # path('sendmail', views.sendmail, name='sendmail'),
     path('usersendmsg', views.usersendmsg, name='usersendmsg'),
     # path('viewfeedbacks', views.viewfeedbacks, name='viewfeedbacks'),
     path('gotoreplyform/<int:sid>/', views.gotoreplyform, name='gotoreplyform'),
     path('sendreplymail', views.sendreplymail, name='sendreplymail'),
     path('getbrand', views.getbrand, name='getbrand'),
     path('deletebrand/<int:bid>/', views.deletebrand, name='deletebrand'),
     path('getvehiclename', views.getvehiclename, name='getvehiclename'),
     path('addvehicle', views.addvehicle, name='addvehicle'),
     path('deletevehiclename/<int:vnid>/', views.deletevehiclename, name='deletevehiclename'),
     path('getvehicleinfo', views.getvehicleinfo, name='getvehicleinfo'),
     path('deletevehicle/<int:vid>/', views.deletevehicle, name='deletevehicle'),
     path('updatevehicle', views.updatevehicle, name='updatevehicle'),

     path('changetosold/<int:sid>/', views.changetosold, name='changetosold'),

     path('gotoupdatevehiclepage/<int:vid>/', views.gotoupdatevehiclepage, name='gotoupdatevehiclepage'),






     # path('test', views.test_management, name='test_management'),
     # path('slot_management', views.slot_management, name='slot_management'),
     # path('cat', views.cat_management, name='cat_management'),
     # path('slot', views.addslot, name='slot'),
     # path('addcat', views.addcat, name='addcat'),
     # path('addtest', views.addtest, name='addtest'),
     # path('gettestdata', views.gettestdata, name='gettestdata'),
     # path('updatetest', views.updatetest, name='updatetest'),
     # path('getupdatedtestdata', views.getupdatedtestdata, name='getupdatedtestdata'),
     # path('updateslot', views.updateslot, name='updateslot'),
     # path('getupdatedslotdata', views.getupdatedslotdata, name='getupdatedslotdata'),
     # path('addslotdata', views.addslotdata, name='addslotdata'),
     # path('deleteslot', views.deleteslot, name='deleteslot'),
     # path('deletetest', views.deletetest, name='deletetest'),
     # path('listcat', views.list_by_cat, name='listcat'),


]