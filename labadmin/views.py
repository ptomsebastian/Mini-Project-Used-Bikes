import os


from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
#from.models import Patient,Slot,Customer,User,Appointment,Category,Feedback,Home,Info,Order,Payment,Result,Test
from .forms import VehicleForm
from.models import User,Brand,Vehiclename,Vehicle,Customer,Feedback,Info,Booking
from django.conf import settings
from django.core.mail import send_mail
from datetime import timedelta, datetime
from django.db.models.functions import Now
from django.utils.timezone import now
import smtplib
from django.db.models import Q



User = get_user_model()

# Create your views here.



def index(request):
    now = datetime.now()
    bh=Booking.objects.filter(created_at__lte=now-timedelta(days=1)) & Booking.objects.filter(status="BOOKED")
    print(bh)
    for x in bh:
        x.status="CANCELLED"
        print(x.updated_at.date())
        x.save()
    for i in bh:
        print(i.vehicle_id)
        vh=Vehicle.objects.get(id=i.vehicle_id)
        vh.status="CANCELLED"
        vh.save()

    home = Info.objects.all().values()
    context = {'home': home}
    return render(request, 'index.html',context)

def signin(request):
    return render(request, '1login.html')

def signup(request):
   return render(request, '1register.html')


def gk_logout(request):
    # Log out the user.
    logout(request)
    now = datetime.now()
    bh=Booking.objects.filter(created_at__lte=now-timedelta(days=1)) & Booking.objects.filter(status="BOOKED")
    print(bh)
    for x in bh:
        x.status="CANCELLED"
        x.save()
    for i in bh:
        print(i.vehicle_id)
        vh=Vehicle.objects.get(id=i.vehicle_id)
        vh.status="CANCELLED"
        vh.save()

    home = Info.objects.all().values()
    context = {'home': home}
    # Return to homepage.
    return render(request, 'index.html',context)


# def lab_logout(request):
#     # Log out the user.
#     logout(request)
#     # Return to homepage.
#     return render(request, 'index.html')


def vehicle_management(request):
    brnd = Brand.objects.all().order_by('name').values()
    vehicles = Vehicle.objects.all().order_by('status')
    vname = Vehiclename.objects.all().values()
    print(vehicles)
    context = {'brnd': brnd,'vehicles':vehicles,'vname': vname}
    return render(request, 'labadmin/6vehicle manage.html',context)

def home_page_management(request):
    home = Info.objects.all().values()
    context = {'home': home}
    return render(request, 'labadmin/8homepageinfo.html', context)

def get_homeimage(request):
    img = request.FILES['image']
    print(img)
    print("hai")
    b = Info()
    b.image=img
    b.title = "BBB"
    b.content = "VVV"
    b.save()
    url = '/home'
    resp_body = '<script>alert("Home image added");\
                            window.location="%s"</script>' % url
    return HttpResponse(resp_body)
    return redirect('home_page_management')

def deletehomeimage(request,hid):
    entry = Info.objects.get(id=hid)
    print(entry)
    entry.delete()
    return redirect('home_page_management')



def book_management(request):
    custid = request.session['uid']
    bk = Booking.objects.all().order_by('-id')
    cus = Customer.objects.filter(id=custid)
    context = {'bk': bk, 'cus': cus}
    return render(request, 'labadmin/9booking.html', context)

def changetosold(request,sid):
    bk = Booking.objects.get(id=sid)
    bk.status="SOLD"
    bk.save()
    vh=Vehicle.objects.get(id=bk.vehicle_id)
    vh.status="SOLD"
    vh.save()
    url = '/book_management'
    resp_body = '<script>alert("Vehicle is SOLD");\
                                window.location="%s"</script>' % url
    return HttpResponse(resp_body)



# def feedback_management(request):
#     return HttpResponse("success")


def business_report(request):
    bk=Booking.objects.filter(status='SOLD').order_by('-updated_at')
    c = bk.count()
    print(c)
    sum = 0
    for i in bk:
        sum = sum + i.vehicle.price

    if request.method=="POST":
        d1=request.POST['startdate']
        bk=Booking.objects.filter((Q(updated_at__contains = d1) & Q(status="SOLD"))).order_by('-updated_at')
        print(bk)
        c=bk.count()
        print(c)
        sum=0
        for i in bk:
            sum=sum+i.vehicle.price

        print(sum)

    context = {'bk': bk,'sum':sum,'count':c}
    return render(request, 'labadmin/10report.html',context)


def brand_management(request):
    brnd = Brand.objects.all().values()
    context = {'brnd': brnd}

    return render(request, 'labadmin/2brand.html', context)

def getbrand(request):
    brand = request.POST['brand']
    print(brand)
    br=Brand.objects.filter(name=brand)
    if len(br)==0:
        b = Brand()
        b.name = brand
        b.save()
        url = '/brand'
        resp_body = '<script>alert("Brand added successfully");\
                                    window.location="%s"</script>' % url
    else:
        url = '/brand'
        resp_body = '<script>alert("Brand already exists!");\
                                    window.location="%s"</script>' % url

    return HttpResponse(resp_body)
    return redirect('brand_management')

   # return HttpResponse("success")

def deletebrand(request,bid):
    entry = Brand.objects.get(id=bid)
    print(entry)
    entry.delete()
    return redirect('brand_management')



def vehicle_name_management(request):
    brnd = Brand.objects.all().order_by('name').values()

    # brnd = Brand.objects.all().values()
    vehiclename = Vehiclename.objects.all().values()

    context = {'brnd': brnd,'vehiclename': vehiclename}
    return render(request, 'labadmin/3vehiclename.html',context)

def getvehiclename(request):
    brand = request.POST['brand']
    print(brand)
    vehiclename = request.POST['Vehicle Name']
    print(vehiclename)
    vn=Vehiclename.objects.filter(name=vehiclename)
    if len(vn)==0:
        b = Vehiclename()
        b.name = vehiclename
        b.brand_id = brand
        b.save()
        url = '/vehiclename'
        resp_body = '<script>alert("Vehicle name added successfully");\
                                window.location="%s"</script>' % url
    else:
        url = '/vehiclename'
        resp_body = '<script>alert("Vehicle name already exists!");\
                                window.location="%s"</script>' % url
    return HttpResponse(resp_body)
    return redirect('vehicle_name_management')

def deletevehiclename(request,vnid):
    entry = Vehiclename.objects.get(id=vnid)
    print(entry)
    entry.delete()
    return redirect('vehicle_name_management')


def logout(request):
    return HttpResponse("success")


def addvehicle(request):
    bid=request.POST['brand']
    request.session['bid']=bid
    # brnd = Brand.objects.order_by('name')[:]
    print(bid)
    #vehiclename = Vehiclename.objects.order_by('name')[:]
    # vehiclename = Vehiclename.objects.get(brand=bid)


    vehiclename = Vehiclename.objects.order_by('name').filter(brand=bid)
    context = {'vehiclename':vehiclename,}
    return render(request, 'labadmin/4addvehicle.html',context)


def deletevehicle(request,vid):
    entry = Vehicle.objects.get(id=vid)
    print(entry)
    entry.delete()
    return redirect('vehicle_management')

# def gotoupdatevehiclepage(request,vid):
#     veh = Vehicle.objects.get(id=vid)
#     request.session['vid'] = vid
#     context = {'veh': veh}
#
#     return render(request,'labadmin/5updatevehicle.html',context)
#
#
# def updatevehicle(request):
#     vid = request.session['vid']
#     b = Vehicle.objects.get(id=vid)
#     print(b)
#
#     vnum = request.POST['vnum']
#     vin = request.POST['vin']
#     cc = request.POST['cc']
#     year = request.POST['year']
#     price = request.POST['price']
#     description = request.POST['description']
#     product1 = request.POST.get('image1', False)
#     product2 = request.POST.get('image2', False)
#     product3 = request.POST.get('image3', False)
#
#
#     #b.brand
#     b.vehiclenumber=vnum
#     b.cc=cc
#     b.vin=vin
#     b.des=description
#     b.year=year
#     b.price=price
#     b.image1=product1
#     b.image2=product2
#     b.image3=product3
#     b.save()
#     #
#     url = '/vehicle'
#     resp_body = '<script>alert("Vehicle updated successfully");\
#                             window.location="%s"</script>' % url
#     return HttpResponse(resp_body)
#
#     print(vehiclename_id,vnum,vin,cc,year,price)
#
#
#     print(vnum,vin,cc,year,price)
#     return redirect('vehicle_management')




def getvehicleinfo(request):
    vehiclename_id = request.POST['vehiclename']
    vnum = request.POST['vnum']
    vin = request.POST['vin']
    cc = request.POST['cc']
    colour = request.POST['colour']
    km = request.POST['km']
    year = request.POST['year']
    price = request.POST['price']
    description = request.POST['description']
    product1 = request.FILES['image1']
    product2 = request.FILES['image2']
    product3 = request.FILES['image3']
    # image = request.POST['image']
    #form = VehicleForm(request.POST, request.FILES)
    # if form.is_valid():
    #     form.save()
    vh=Vehicle.objects.filter(vehiclenumber=vnum)
    if len(vh)==0:
        b = Vehicle()
        # b.brand
        b.vehiclenumber = vnum
        b.cc = cc
        b.colour = colour
        b.km = km
        b.vin = vin
        b.des = description
        b.year = year
        b.price = price
        b.image1 = product1
        b.image2 = product2
        b.image3 = product3
        b.vehiclename_id_id = vehiclename_id
        b.save()
        #
        url = '/vehicle'
        resp_body = '<script>alert("Vehicle added successfully");\
                                window.location="%s"</script>' % url
        return HttpResponse(resp_body)

    else:
        url = '/vehicle'
        resp_body = '<script>alert("Vehicle already exists");\
                                          window.location="%s"</script>' % url
        return HttpResponse(resp_body)



    # print(vehiclename_id,vnum,vin,cc,year,price)
    # return redirect('vehicle_management')





def gotoupdatevehiclepage(request,vid):
    veh = Vehicle.objects.get(id=vid)
    request.session['vid'] = vid
    context = {'veh': veh}
    print(veh)

    return render(request,'labadmin/5updatevehicle.html',context)


def updatevehicle(request):
    vid = request.session['vid']
    b = Vehicle.objects.get(id=vid)
    print(b)
    if request.method=="POST":
        # if len(request.FILES) !=0:
        #     if len(b.image1)>0:
        #         os.remove(b.image1.path)
            # elif len(b.image2)>0:
            #     os.remove(b.image2.path)
            # elif len(b.image3)>0:
            #     os.remove(b.image3.path)

        vnum = request.POST['vnum']
        vin = request.POST['vin']
        cc = request.POST['cc']
        colour = request.POST['colour']
        km = request.POST['km']
        year = request.POST['year']
        price = request.POST['price']
        description = request.POST['description']
        product1 = request.FILES.get('image1')
        product2 = request.FILES.get('image2')
        product3 = request.FILES.get('image3')

        # b.brand
        b.vehiclenumber = vnum
        b.cc = cc
        b.colour = colour
        b.km = km
        b.vin = vin
        b.des = description
        b.year = year
        b.price = price
        b.image1 = product1
        b.image2 = product2
        b.image3 = product3
        b.save()
        #
        url = '/vehicle'
        resp_body = '<script>alert("Vehicle updated successfully");\
                                window.location="%s"</script>' % url
        return HttpResponse(resp_body)

        # print(vehiclename_id, vnum, vin, cc, year, price)

    # print(vnum, vin, cc, year, price)
    return redirect('vehicle_management')










# def test_management(request):
#     catgry = Category.objects.order_by('name')[:]
#     context = {'catgry': catgry}
#     return render(request, 'labadmin/test manage.html',context)
#
# def slot_management(request):
#     return render(request, 'labadmin/slot manage.html')
#
# def cat_management(request):
#     #catgry = Category.objects.all().values()
#    # context = {
#     #    'catgry ': catgry,
#     #}
#     #catgry = get_object_or_404(Category)
#     #context = {' catgry':  catgry}
#     catgry = Category.objects.order_by('name')[:]
#     context = {'catgry': catgry}
#     return render(request, 'labadmin/category.html', context)
#
#    # return render(request, 'category.html')
#
# def list_by_cat(request):
#     cat_id = request.GET['cat_id']
#     cat = Test.objects.filter(category_id=cat_id)
#     qs_json = serialize('json', cat)
#     print(qs_json)
#     return JsonResponse({"testresult": qs_json})



def register(request):


    return render(request, '1register.html')

def getregisterdata (request):
    name = request.POST['name']
    addr = request.POST['addr']
    gen = request.POST['gender']
    phone = request.POST['mob']
    email = request.POST['email']
    passwd = request.POST['pwd']
    print(name,addr,gen,phone,email,passwd)
    p=make_password(passwd)
    em = User.objects.filter(email=email)
    if len(em)==0:
        u = User()
        u.email = email
        u.password = p
        u.username = email
        u.first_name = name
        u.last_name = name
        u.user_type = "customer"
        u.save()

        uid = User.objects.filter(email=email).values('id')
        print(uid)
        # x = User.objects.filter(email=email)
        # print(x)
        # print(x['id'])
        z = None
        for i in uid:
            z = i.get('id')
        print(z)
        c = Customer()
        c.user_id = z
        c.name = name
        c.address = addr
        c.gender = gen
        c.phone = phone
        c.save()
        url = '/signup'
        resp_body = '<script>alert("Registered Successfully");\
                                window.location="%s"</script>' % url
        return HttpResponse(resp_body)

    url = '/signup'
    em_body = '<script>alert("Email id already exists!");\
                            window.location="%s"</script>' % url
    return HttpResponse(em_body)
    return redirect('register')








def login_user(request):
    email = request.POST['username']
    password = request.POST['password']
    try:
        usr = User.objects.get(email=email)
    except User.DoesNotExist:
        usr = None

    if(usr):

        user = authenticate(username=usr.username, password=password)

        if user is not None:
            usertype = user.user_type

            if usertype == "shopowner":
                return render(request, 'index2.html')

            # elif usertype == 'resp':
            #     return render(request, '')

            elif usertype == 'customer':

                customer = Customer.objects.get(user_id=user.id)
                print(customer.id)
                if (customer):

                    request.session['uid'] = customer.id
                    request.session['uname'] = customer.name
                    # login(request, user)
                    # return render(request, 'customer/user dash.html', context)
                    context={'customer':customer}
                    return render(request, 'index3.html',context)

                else:
                    return HttpResponse('User not found!')

                # return render(request, 'mysite/customer/templates/user dash.html')
            else:
                return HttpResponse('Invalid user!')


        else:
            url = 'signin'
            resp_body = '<script>alert("Login error");\
                                                   window.location="%s"</script>' % url
            return HttpResponse(resp_body)

        # else:
        #     return HttpResponse('login error!')


    url = 'signin'
    resp_body = '<script>alert("Invalid username or password!");\
                                                       window.location="%s"</script>' % url
    return HttpResponse(resp_body)


    # username = User.objects.get(email=email).username
    # user = authenticate(username=username, password=password)





def usersendmsg(request):
    name = request.POST['name']
    eml = request.POST['email']
    subject = request.POST['subject']
    msg = request.POST['message']
    fdbk=Feedback()
    fdbk.name = name
    fdbk.email = eml
    fdbk.subject = subject
    fdbk.message = msg
    fdbk.reply = "pending"
    fdbk.save()
    url = '/'
    resp_body = '<script>alert("Message Send Successfully");\
                                   window.location="%s"</script>' % url
    return HttpResponse(resp_body)


    # return redirect('index')

# def feedback_management(request):
#     return HttpResponse("success")

# def viewfeedbacks(request):
#     fdbk=Feedback.objects.filter(reply="pending")
#
#     context={'fdbk':fdbk}

    # return render(request,'labadmin/feedback.html',context)

def feedback_management(request):
    fdbk=Feedback.objects.filter(reply="pending")

    context={'fdbk':fdbk}

    return render(request,'labadmin/feedback.html',context)

def gotoreplyform(request,sid):
    request.session['senderid']=sid
    feedbackobj=Feedback.objects.get(id=sid)
    context={'feedbackobj':feedbackobj}

    return render(request,'labadmin/replyform.html',context)


def sendreplymail(request):
    # print("hai")
    sid = request.session['senderid']
    subj= Feedback.objects.filter(id=sid).values('subject')

    # sub=request.POST['subject']
    msg = request.POST['content']

    feedbackobj = Feedback.objects.get(id=sid)
    em=feedbackobj.email
    subj = feedbackobj.subject
    feedbackobj.reply=msg
    feedbackobj.save()

    # subject = sub
    message = msg
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [em,]
    server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    send_mail(subj, message, email_from, recipient_list)

    url = '/feedback'
    resp_body = '<script>alert("Reply send");\
                                       window.location="%s"</script>' % url
    return HttpResponse(resp_body)






# def addcat(request):
#     cat = request.POST['category']
#     print(cat)
#     p = Category(name=cat)
#     p.save()
#     #catgry = Category.objects.all().values()
#     #print(catgry)
#     catgry = Category.objects.order_by('name')[:]
#     context = {'catgry': catgry}
#     return render(request, 'labadmin/category.html', context)
#
# def addtest(request):
#
#     #catgry = Category.objects.all().values()
#     #print(catgry)
#    # catgry = Category.objects.order_by('name')[:]
#     #context = {'catgry': catgry}
#     catgry = Category.objects.order_by('name')[:]
#     context = {'catgry': catgry}
#     return render(request, 'labadmin/addtest.html', context)
#
# def gettestdata(request):
#
#     tname = request.POST['test']
#     des = request.POST['testdes']
#     price = request.POST['price']
#     cat = request.POST['category']
#     tavail = request.POST.getlist('available')
#     havail = request.POST.getlist('home')
#     print(cat)
#
#     if(len(tavail)==0):
#
#         ts="false"
#     else:
#         ts="true"
#
#     if (len(havail) == 0):
#
#         hs = "false"
#     else:
#         hs = "true"
#
#     c = Test()
#     c.name = tname
#     c.price=price
#     c.des=des
#     c.status=ts
#     c.hstatus=hs
#     c.category_id=cat
#     c.save()
#
#     return redirect('test_management')
#
# def updatetest(request):
#     catgry = Category.objects.order_by('name')[:]
#     context = {'catgry': catgry}
#
#     return render(request, 'labadmin/update test.html',context)
#
#
# def getupdatedtestdata(request):
#     tname = request.POST['test']
#     des = request.POST['testdes']
#     price = request.POST['price']
#     cat = request.POST['category']
#     tavail = request.POST.getlist('available')
#     havail = request.POST.getlist('home')
#
#     print(tname,des,price,cat,tavail,havail)
#
#     catgry = Category.objects.order_by('name')[:]
#     context = {'catgry': catgry}
#     return render(request,'labadmin/test manage.html',context)
#
#
# def updateslot(request):
#
#
#     return render(request, 'labadmin/update slot.html')
#
# def getupdatedslotdata(request):
#     #slot_interval = request.POST['slot_interval']
#     #strength = request.POST['strength']
#     #status = request.POST.getlist('slot_status')
#
#
#     return render(request, 'labadmin/slot manage.html')
#
#
# def addslot(request):
#
#
#     return render(request, 'labadmin/add slot.html')
#
# def addslotdata(request):
#     #slot_interval = request.POST['slot_interval']
#     #strength = request.POST['strength']
#     #status = request.POST.getlist('slot_status')
#     return render(request, 'labadmin/slot manage.html')
#
# def deleteslot(request):
#
#     return render(request, 'labadmin/slot manage.html')
#
#
# def deletetest(request):
#
#     return render(request, 'labadmin/test manage.html')








