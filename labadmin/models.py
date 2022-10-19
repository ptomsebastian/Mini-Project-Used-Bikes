from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    user_type = models.CharField(max_length=20)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=60)
    gender = models.CharField(max_length=6)
    phone = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #    return self.name

class Brand(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Vehiclename(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    vehiclename_id= models.ForeignKey(Vehiclename, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='images/', null=True, max_length=255)
    image2 = models.ImageField(upload_to='images/', null=True, max_length=255)
    image3 = models.ImageField(upload_to='images/', null=True, max_length=255)
    vehiclenumber = models.CharField(max_length=25)
    vin = models.CharField(max_length=25)
    colour = models.CharField(max_length=25, default='')
    km = models.IntegerField(default='100')
    year= models.IntegerField()
    price = models.IntegerField()
    des = models.CharField(max_length=100)
    cc = models.IntegerField()
    status = models.CharField(max_length=15, default='')
    #hstatus = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return '%s %s' %(self.brand, self.name)

class Info(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=60)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    #bdate = models.DateField()
    #mode = models.CharField(max_length=15)
    #token = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.CharField(max_length=60)
    reply = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,default="")
    amount = models.FloatField(default=0.0)
    transaction = models.CharField(max_length=200)
    status = models.CharField(max_length=45, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)















#gsy-code
class Category(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
#
# class Test(models.Model):
#     name = models.CharField(max_length=30)
#     price = models.IntegerField()
#     des = models.CharField(max_length=100)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     status = models.CharField(max_length=15)
#     hstatus = models.CharField(max_length=15)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#
#     def __str__(self):
#         return '%s %s' %(self.category, self.name)
#
#
# class Slot(models.Model):
#     time = models.CharField(max_length=10)
#     status = models.CharField(max_length=15)
#     strength = models.PositiveIntegerField(default=0)
#     astrength = models.PositiveIntegerField(default=0)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return '%s %s' %(self.category, self.time)
#
#
# class Patient(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     pname = models.CharField(max_length=25)
#     age = models.PositiveIntegerField(default=0)
#     gender = models.CharField(max_length=6)
#     phone = models.BigIntegerField()
#     testpres = models.FileField()
#     place = models.CharField(max_length=25)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.pname
#
#
# class Appointment(models.Model):
#     patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
#     bdate = models.DateField()
#     mode = models.CharField(max_length=15)
#     token = models.PositiveIntegerField(default=0)
#     status = models.CharField(max_length=20)
#     testpres = models.FileField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.patient
#
#
# class Order(models.Model):
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
#     tests = models.ForeignKey(Test,  on_delete=models.CASCADE)
#     slot=models.ForeignKey(Slot, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return '%s %s' %(self.appointment, self.tests)
#
# class Feedback(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     message = models.CharField(max_length=60)
#     reply = models.CharField(max_length=60)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.customer
#
#
# class Home(models.Model):
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
#     lat = models.DecimalField(max_digits=22,decimal_places=16)
#     lon = models.DecimalField(max_digits=22, decimal_places=16)
#     status = models.CharField(max_length=20)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.appointment
#
# class Info(models.Model):
#     title = models.CharField(max_length=20)
#     content = models.CharField(max_length=60)
#     image = models.ImageField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.title
#
#
# class Payment(models.Model):
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
#     amount = models.FloatField(default=0.0)
#     transaction = models.CharField(max_length=200)
#     status = models.CharField(max_length=45, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.appointment
#
#
# class Result(models.Model):
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
#     file = models.FileField()
#     status = models.CharField(max_length=15)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.appointment




