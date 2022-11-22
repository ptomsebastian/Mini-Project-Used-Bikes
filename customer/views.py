from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client

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
Payment = apps.get_model('labadmin', 'Payment')

#Razorpay
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def index(request):
    # print("hai")
    return render(request, '/labadmin/templates/login.html')

# def profile(request):
#     return HttpResponse("success")



def editprofile(request):
    uid = request.session['uid']
    # print(uid)
    usr = Customer.objects.get(id=uid)
    print(usr.id)
    print(usr.user_id)
    p1 = 0

    if usr.gender == "male":
        p1 = 1

    useremail=User.objects.get(id=usr.user_id)


    context={'usr':usr,'useremail':useremail,'p1':p1}


    return render(request,'customer/update profile.html',context)



def getupdatedprofile(request):
    uid = request.session['uid']
    # print(uid.id)
    name = request.POST['name']
    addr = request.POST['addr']
    gen = request.POST['gender']
    phone = request.POST['mob']
    email = request.POST['email']
    passwd = request.POST['pwd']
    print(name, addr, gen, phone, email, passwd)
    usr = Customer.objects.get(id=uid)
    usr.name=name
    usr.address=addr
    usr.gender=gen
    usr.phone=phone
    usr.save()
    p = make_password(passwd)
    usr1=User.objects.get(id=usr.user_id)
    # print(usr1)
    usr1.password=p
    usr1.username=email
    usr1.first_name=name
    usr1.last_name = name
    usr1.email = email
    usr1.save()
    url = '/customer/editprofile'
    resp_body = '<script>alert("Profile updated successfully");\
                            window.location="%s"</script>' % url
    return HttpResponse(resp_body)


def vehicles(request):
    brnd = Brand.objects.all().order_by('name').values()
    vehicles = Vehicle.objects.all().exclude(status="BOOKED") & Vehicle.objects.all().exclude(status="SOLD")
    vname = Vehiclename.objects.all().values()
    # print(vehicles)
    context = {'brnd': brnd, 'vehicles': vehicles, 'vname': vname}
    return render(request, 'customer/1viewvehicles.html', context)


def cart(request):
    custid = request.session['uid']
    crt=Cart.objects.filter(customer_id=custid)
    li=[]
    for a in crt:
        li.append(a.vehicle_id)
    print(li)

    # print(crt)
    vehi=list(Vehicle.objects.all().order_by('vehiclenumber').values())
    vehi2=Vehicle.objects.all()
    # print(vehi)
    # for x in crt:
    #     for i in vehi:
    #         if x.customer_id == i.id:
    #             print(i.vehiclenumber)

    l=[]
    for x in vehi:
        for key,val in x.items():
            # print(key,val)
            if key == 'id':
                l.append(val)
    # print(l)

    brnd=Brand.objects.all()
    vname=Vehiclename.objects.all()
    for i in crt:
        for j in vehi2:
            for k in vname:
                if k.id == j.vehiclename_id_id:
                    if j.id == i.vehicle_id:
                        print(k.name)

    context = {'crt':crt,'vehi':vehi,'li':li,'vehi2':vehi2,'vname':vname,'brnd':brnd}
    return render(request, 'customer/3cart.html',context)


# def payment(request):
#     bk = Booking().objects.all()
#     pay = Payment()
#     pay.booking_id=bk.booking_id
#     pay.status = bk.status
#     pay.amount="10"
#     pay.save()
#     return redirect('view_bookings')
#     # return redirect('home')


def deletefromcart(request,cid):
    custid = request.session['uid']

    # print('hai')
    # ca=Cart.objects.all()
    # ca.delete()

    c=Cart.objects.filter(id=cid) & Cart.objects.filter(customer_id=custid)
    c.delete()

    # c=Cart.objects.get(vehicle_id=dcartid) & Cart.objects.get(customer_id=custid)
    # c.delete()
    return redirect('cart')



def view_bookings(request):
    custid = request.session['uid']
    bk = Booking.objects.filter(customer_id=custid).order_by('-id')
    cus = Customer.objects.filter(id=custid)
    # request.session['vmoreid'] = vmoreid
    # print(vmoreid)
    # vh = Vehicle.objects.get(id=vmoreid)
    # vmname = Vehiclename.objects.get(id=vh.vehiclename_id_id)
    context = {'bk': bk,'cus':cus}
    return render(request, 'customer/4bookings.html',context)
    # print(context)
    # return render(request, 'labadmin/2brand.html', context)


def feedback(request):
    return HttpResponse("success")


def viewmorevehicledetails(request,vmoreid):
    request.session['vmoreid'] = vmoreid
    print(vmoreid)
    vh = Vehicle.objects.get(id=vmoreid)

    vmname = Vehiclename.objects.get(id=vh.vehiclename_id_id)
    brandname = Brand.objects.get(id=vmname.brand_id)
    print(vmname.name)
    print(brandname.name)
    context = {'vh':vh, 'vmname':vmname,'brandname':brandname}

    return render(request,'customer/2selectedvehicle.html',context)

def addtocart(request,vhid):
    custid = request.session['uid']
    print(custid)
    x = Cart.objects.filter(vehicle_id=vhid) & Cart.objects.filter(customer_id=custid)
    print(x)
    if len(x)==0:
        c = Cart()

        c.customer_id = custid
        c.vehicle_id = vhid
        c.save()
        url = '/customer/cart'
        resp_body = '<script>alert("Vehicle added to cart successfully");\
                                window.location="%s"</script>' % url
        return HttpResponse(resp_body)
        return redirect('cart')
    else:
        # return HttpResponse("The vehicle already exist!!")
        url = '/customer/cart'
        resp_body = '<script>alert("Vehicle already exists!!");\
                                window.location="%s"</script>' % url
        return HttpResponse(resp_body)



def vbook2(request, bvhid2):
    request.session['cartid']=bvhid2
    vh=Cart.objects.get(id=bvhid2)
    print(vh.vehicle_id)

    print(bvhid2)
    request.session['bvid2'] = vh.vehicle_id
    print("haiiii")
    return redirect('home2')


#payment portion for CART
def home2(request):
    bvid2 = request.session['bvid2']
    amt=Vehicle.objects.get(id=bvid2)
    request.session['advamount']=amt.price

    print("haiiii")
    currency = 'INR'
    amount = (amt.price)*5  # Rs. 200
    print(amount)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler2'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'payment.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.


@csrf_exempt
def paymenthandler2(request):
    cid = request.session['cartid']
    amt=request.session['advamount']
    uid = request.session['uid']
    # bvid = request.session['bvid']
    bvid2 = request.session['bvid2']
    # only accept POST request.
    print('fff')
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = amt*5  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    bk= Booking()
                    bk.customer_id=uid
                    bk.vehicle_id=bvid2
                    bk.status="BOOKED"
                    bk.save()

                    bookid = (Booking.objects.last()).id
                    pay = Payment()
                    pay.booking_id = bookid
                    pay.transaction = payment_id
                    pay.status = "BOOKED"
                    pay.amount = amt
                    pay.save()
                    c=Cart.objects.get(id=cid)
                    c.delete()


                    vnum=Vehicle.objects.get(id=bvid2)
                    vnum.status="BOOKED"
                    vnum.save()
                    cus=Customer.objects.get(id=uid)
                    paid = (amt * 5) / 100

                    smsmsg ='BOOKING RECEIPT \n****************************** \nBooking ID: ' + str(bookid) + '\n\nCustomer Name: ' + cus.name + '\n\nVehicle Number: ' + vnum.vehiclenumber + '\n\nAmount Paid: ' + str(paid) + '\n******************************'
                    mob = '+91' + str(7510734911)
                    account_sid = 'ACf4cff537e8e5e8fadbb9965acb4b0959'
                    auth_token = '421f07f38492519a00c85d10bc96ab72'
                    client = Client(account_sid, auth_token)

                    message = client.messages.create(

                        body=smsmsg,
                        from_='+12057362452',
                        to = mob

                    )

                    url = '/customer/view_bookings'
                    resp_body = '<script>alert("Booked successfully");\
                                                    window.location="%s"</script>' % url
                    return HttpResponse(resp_body)


                    # return HttpResponse('success')
                except:
                    bk= Booking()
                    bk.status="FAILED"
                    bk.save()

                    bookid = (Booking.objects.last()).id
                    pay = Payment()
                    pay.status = "FAILED"
                    pay.save()

                    # if there is an error while capturing payment.
                    resp_body = '<script>alert("payment failed...");\
                                                                     </script>'
                    return HttpResponse(resp_body)
            else:

                # if signature verification fails.
                resp_body = '<script>alert("payment failed...");\
                                                    </script>'
                return HttpResponse(resp_body)
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()








#DIRECT BOOKING

def vbook1(request, bvhid):
    print(bvhid)
    request.session['bvid'] = bvhid
    print("haiiii")

    return redirect('home')



#payment portion
def home(request):
    bvid = request.session['bvid']
    amt=Vehicle.objects.get(id=bvid)
    request.session['advamount']=amt.price

    print("haiiii")
    currency = 'INR'
    amount = (amt.price)*5  # Rs. 200
    print(amount)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'payment.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.


@csrf_exempt
def paymenthandler(request):
    amt=request.session['advamount']
    uid = request.session['uid']
    # bvid = request.session['bvid']
    bvid = request.session['bvid']
    # only accept POST request.
    print('fff')
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = amt*5  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    bk= Booking()
                    bk.customer_id=uid
                    bk.vehicle_id=bvid

                    bk.status="BOOKED"
                    bk.save()

                    bookid = (Booking.objects.last()).id
                    pay = Payment()
                    pay.booking_id = bookid
                    pay.transaction = payment_id
                    pay.status = "BOOKED"
                    pay.amount = amt
                    pay.save()

                    vnum = Vehicle.objects.get(id=bvid)
                    vnum.status="BOOKED"
                    vnum.save()
                    cus = Customer.objects.get(id=uid)
                    paid= (amt * 5)/100


                    smsmsg ='BOOKING RECEIPT \n****************************** \nBooking ID: ' + str(bookid) + '\n\nCustomer Name: ' + cus.name + '\n\nVehicle Number: ' + vnum.vehiclenumber + '\n\nAmount Paid: ' + str(paid) + '\n******************************'
                    mob = '+91' + str(7510734911)
                    account_sid = 'ACf4cff537e8e5e8fadbb9965acb4b0959'
                    auth_token = '421f07f38492519a00c85d10bc96ab72'
                    client = Client(account_sid, auth_token)

                    message = client.messages.create(

                        body=smsmsg,
                        from_='+12057362452',
                        to = mob

                    )
                    url = '/customer/view_bookings'
                    resp_body = '<script>alert("Booked successfully");\
                                                    window.location="%s"</script>' % url
                    return HttpResponse(resp_body)

                    # return HttpResponse('success')
                except:
                    bk= Booking()
                    bk.status="FAILED"
                    bk.save()

                    bookid = (Booking.objects.last()).id
                    pay = Payment()
                    pay.status = "FAILED"
                    pay.save()

                    # if there is an error while capturing payment.
                    resp_body = '<script>alert("payment failed...");\
                                                                     </script>'
                    return HttpResponse(resp_body)
            else:

                # if signature verification fails.
                resp_body = '<script>alert("payment failed...");\
                                                    </script>'
                return HttpResponse(resp_body)
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
