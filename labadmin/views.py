from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
#from.models import Patient,Slot,Customer,User,Appointment,Category,Feedback,Home,Info,Order,Payment,Result,Test
from .forms import VehicleForm
from.models import User,Brand,Vehiclename,Vehicle,Customer

User = get_user_model()

# Create your views here.



def index(request):
    return render(request, 'index.html')

def signin(request):
    return render(request, '1login.html')

def signup(request):
   return render(request, '1register.html')


def vehicle_management(request):
    brnd = Brand.objects.all().order_by('name').values()
    vehicles = Vehicle.objects.all().values()
    vname = Vehiclename.objects.all().values()
    print(vehicles)
    context = {'brnd': brnd,'vehicles':vehicles,'vname': vname}
    return render(request, 'labadmin/6vehicle manage.html',context)

def home_page_management(request):
    return HttpResponse("success")

def book_management(request):
    return HttpResponse("success")

def feedback_management(request):
    return HttpResponse("success")

def business_report(request):
    return HttpResponse("success")

def brand_management(request):
    brnd = Brand.objects.all().values()
    context = {'brnd': brnd}

    return render(request, 'labadmin/2brand.html', context)

def getbrand(request):
    brand = request.POST['brand']
    print(brand)
    b=Brand()
    b.name=brand
    b.save()
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
    b=Vehiclename()
    b.name=vehiclename
    b.brand_id=brand
    b.save()
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

def gotoupdatevehiclepage(request,vid):
    veh = Vehicle.objects.get(id=vid)
    request.session['vid'] = vid
    context = {'veh': veh}

    return render(request,'labadmin/5updatevehicle.html',context)


def updatevehicle(request):
    vid = request.session['vid']
    b = Vehicle.objects.get(id=vid)
    print(b)

    vnum = request.POST['vnum']
    vin = request.POST['vin']
    cc = request.POST['cc']
    year = request.POST['year']
    price = request.POST['price']
    description = request.POST['description']
    product1 = request.POST.get('image1', False)
    product2 = request.POST.get('image2', False)
    product3 = request.POST.get('image3', False)
    # product1 = request.FILES['image1']
    # product2 = request.FILES['image2']
    # product3 = request.FILES['image3']
    # image = request.POST['image']
    #form = VehicleForm(request.POST, request.FILES)
    # if form.is_valid():
    #     form.save()

    #b.brand
    b.vehiclenumber=vnum
    b.cc=cc
    b.vin=vin
    b.des=description
    b.year=year
    b.price=price
    b.image1=product1
    b.image2=product2
    b.image3=product3
    b.save()
    #

    print(vnum,vin,cc,year,price)
    return redirect('vehicle_management')




def getvehicleinfo(request):
    vehiclename_id = request.POST['vehiclename']
    vnum = request.POST['vnum']
    vin = request.POST['vin']
    cc = request.POST['cc']
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

    b=Vehicle()
    #b.brand
    b.vehiclenumber=vnum
    b.cc=cc
    b.vin=vin
    b.des=description
    b.year=year
    b.price=price
    b.image1=product1
    b.image2=product2
    b.image3=product3
    b.vehiclename_id_id=vehiclename_id
    b.save()
    #

    print(vehiclename_id,vnum,vin,cc,year,price)
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

    u=User()
    u.email=email
    u.password=p
    u.username=email
    u.first_name=name
    u.last_name=name
    u.user_type="customer"
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
    c=Customer()
    c.user_id=z
    c.name=name
    c.address=addr
    c.gender=gen
    c.phone=phone
    c.save()

    return redirect('register')








def login(request):
    email = request.POST['username']
    password = request.POST['password']

    username = User.objects.get(email=email).username
    user = authenticate(username=username, password=password)



    if user is not None:
        usertype = user.user_type

        if usertype == "shopowner":
            return render(request, 'index2.html')

        # elif usertype == 'resp':
        #     return render(request, '')
        elif usertype == 'customer':

            return render(request, 'index3.html')
           #return render(request, 'mysite/customer/templates/user dash.html')
        else:
            return HttpResponse('Invalid user!')

    else:
        return HttpResponse('login error!')



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








