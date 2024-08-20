from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from ims import settings
from ims_app.models import Product,categories,documents
from django.core.mail import send_mail
import time
from django.db.models import Q
from datetime import date, datetime
from qrcode import *
import random
from ims_app.forms import UserRegistrationForm

 
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            if user.account_type == 'admin':
                username=user.get_username
                return redirect("/dashboard")
            elif user.account_type =='employees':
                username=user.get_username
                return redirect("/index")
            elif user.account_type =='manager':
                username=user.get_username
                return redirect("/dashboard")
        else:
            error="wrong"
            return render(request,'html/login.html',{"error":error})
    return render(request, 'html/login.html')

def add_user(request):
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Registration succesfull")
                return redirect("/login")
            else:
                form = UserRegistrationForm()
                messages.error(request,"Registration failed")
                return render(request,"html/add_user.html",{'form': form})
        form = UserRegistrationForm()
        return render(request,"html/add_user.html",{'form': form})

@login_required  
def delete_product(request, product_number):
    product = get_object_or_404(Product, product_number=product_number)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})

@login_required
def update_description(request):
    if request.method == 'POST':
        number=request.POST.get('batch_number')
        upd=Product.objects.get(batch_number=number)
        upd.description=request.POST.get('description')
        upd.save()
        messages.success(request, "Record updated")
        return redirect("/index")
    else:
        messages.error('failed to update')
        return redirect('/index')


@login_required  
def index(request):
    if request.method == 'POST':
        search = request.POST['search']
        Products=Product.objects.filter(name__icontains=search)|Product.objects.filter(batch_number__icontains=search)
        if Products:
            context = {'Products': Products}
            return render(request, 'html/index.html', context)
        else:
            return render(request, 'html/index.html', {'message': 'NO RECORD FOUND.'})
    else:
        return render(request, 'html/index.html')


@login_required  
def signout(request):
        logout(request)
        return redirect('/login')

@login_required  
def dashboard(request):
    role=request.user.account_type
    if role == 'admin':
        if request.method == 'POST':
            prod=Product()
            prod.name=request.POST.get('name')
            prod.price=request.POST.get('price')
            prod.batch_number=request.POST.get('batch_no')
            prod.expirydate=request.POST.get('expiry')
            prod.tquantity=request.POST.get('quantity')
            prod.category=request.POST.get('category')
            prod.save()
            messages.success(request,"Added succesfully")
        else:
            cats=categories.objects.all()
            records=Product.objects.all()
            for item in records:
                item.days_left = (item.expirydate - datetime.now().date()).days
                if item.days_left > 30:
                    item.status = "Safe"
                elif 0 <= item.days_left <= 30:
                    item.status = "Near Expiry"
                else:
                    item.status = "Expired"
            return render(request,"html/dashboard.html",{'record':records,'categories':cats})
        cats=categories.objects.all()
        records=Product.objects.all()
        return render(request,"html/dashboard.html",{'record':records,'categories':cats})
    else:
        return redirect('/login')
    
def search(request):
         if request.method == 'POST':
            search = request.POST['search']
            Products=Product.objects.filter(name__icontains=search)|Product.objects.filter(batch_number__icontains=search)
            if Products:
                for item in Products:
                    item.days_left = (item.expirydate - datetime.now().date()).days
                    if item.days_left > 30:
                        item.status = "Safe"
                    elif 0 <= item.days_left <= 30:
                        item.status = "Near Expiry"
                    else:
                        item.status = "Expired"
                cats=categories.objects.all()
                context = {'Products': Products , 'categories':cats}
                return render(request, 'html/dashboard.html', context)

@login_required      
def update(request,id):
    update=Product.objects.get(id=id)
    records=Product.objects.all()
    return render(request, "html/update.html",{"upd":update,'record':records})

@login_required  
def updated(request, batch_number):
    if request.method == 'POST':
        upd=Product.objects.get(batch_number=batch_number)
        upd.name=request.POST.get('name')
        upd.price=request.POST.get('price')
        upd.batch_number=request.POST.get('batch_no')
        upd.expirydate=request.POST.get('expiry')
        upd.tquantity=request.POST.get('quantity')
        upd.category=request.POST.get('category')
        upd.save()
        messages.success(request, "Record updated")
        return redirect("/dashboard")

@login_required  
def delete(request,id):
    remove=Product.objects.get(id=id)
    remove.delete()
    return redirect("/dashboard")

@login_required  
def delete2(request,number):
    remove=documents.objects.get(document_number=number)
    remove.delete()
    return redirect("/report")

@login_required  
def analytics(request):
    role=request.user.account_type
    if role == 'admin':
        count_all= Product.objects.count()
        days_left =Product.objects.filter(category__contains ='EDIBLES')
        near_Expiry =0
        expired = 0
        count=0
        today = date.today()
        for day in days_left:
            dl=(day.expirydate - today).days
            count+=1
            if dl < 30:
                near_Expiry += 1
            if dl <= 0:
                expired+= 1

        days_left2 =Product.objects.filter(category__contains ='VEHICLES')
        near_Expiry2=0
        expired2 = 0
        count2=0
        today2 = date.today()
        for day2 in days_left2:
            dl2=(day2.expirydate - today2).days
            count2+=1
            if dl2 < 30:
                near_Expiry2 += 1
            if dl2 <= 0:
                expired2+= 1

        days_left3 =Product.objects.filter(category__contains ='RAW MATERIALS')
        near_Expiry3=0
        expired3 = 0
        count3=0
        today3 = date.today()
        for day3 in days_left3:
            dl3=(day3.expirydate - today3).days
            count3+=1
            if dl3 < 30:
                near_Expiry3 += 1
            if dl3 <= 0:
                expired3+= 1
        days_left4 =Product.objects.filter(category__contains ='MEDICAL ITEMS')
        near_Expiry4=0
        expired4 = 0
        count4=0
        today4 = date.today()
        for day4 in days_left4:
            dl4=(day4.expirydate - today4).days
            count4+=1
            if dl4 < 30:
                near_Expiry4 += 1
            if dl4 <= 0:
                expired4+= 1

        days_left5 =Product.objects.filter(category__contains ='TOOLS / EQUIPMENTS')
        near_Expiry5=0
        expired5 = 0
        count5=0
        today5 = date.today()
        for day5 in days_left5:
            dl5=(day5.expirydate - today5).days
            count5+=1
            if dl5 < 30:
                near_Expiry5 += 1
            if dl5 <= 0:
                expired5+= 1
        return render (request, "html/analysis.html",{'count':count,'count2':count2,'count3':count3 ,'count4':count4 ,'count5':count5 ,'near_expiry':near_Expiry,'expired':expired,'near_expiry2':near_Expiry2,'expired2':expired2,'near_expiry3':near_Expiry3,'expired3':expired3,'near_expiry4':near_Expiry4,'expired4':expired4,'near_expiry5':near_Expiry5,'expired5':expired5})
    else:
        redirect('/login')

@login_required  
def category(request):
    role=request.user.account_type
    if role == 'admin':
        if request.method == 'POST':
            cat=categories()
            cat.name=request.POST.get('name')
            cat.description=request.POST.get('description')
            cat.save()
            messages.success(request,"Added succesfully")
        cats=categories.objects.all()
        if request.method == "POST" :
            category_g=request.POST.get('category_name')
            prods=Product.objects.filter(category__contains=category_g)
            if prods:
                return render(request, "html/category.html",{'category':cats , 'prods':prods})
        return render(request, "html/category.html",{'category':cats })
    else:
        redirect('/login')

def get_category_products(request):
    category_name = request.GET.get('category')
    products = Product.objects.filter(category=category_name).values('batch_number', 'name', 'description')
    return JsonResponse({'products': list(products)})

@login_required  
def report(request):
    role=request.user.account_type
    if role == 'admin':
        if request.method == 'POST':
            cat=documents()
            cat.amount=request.POST.get('doc_amount')
            cat.companyname=request.POST.get('doc_company')
            cat.companyaddress=request.POST.get('doc_address')
            cat.quantity=request.POST.get('doc_quantity')
            cat.document_type=request.POST.get('doc_type')
            cat.description=request.POST.get('doc_description')
            cat.document_number=request.POST.get('doc_number')
            cat.save()
            messages.success(request,"Added succesfully")

        products = Product.objects.all()
        for product in products:
            if product.tquantity < 20:
                po = documents()
                po.amount = product.price * (20 - product.tquantity)
                po.companyname = 'THE TIMI COMPANY'
                po.companyaddress = 'ABUJA'
                po.quantity = 20 - product.tquantity
                po.document_type = 'Purchase Order'
                po.description = f'Automatic purchase order for {product.name}'
                po.document_number = f'PO-{product.id}-{product.tquantity}'
                po.save()
                upd=Product.objects.get(name=product.name)
                upd.tquantity+=19
                upd.save()


        docs=documents.objects.all()
        return render(request, "html/report.html",{'docs':docs} )
    else:
        redirect('/login')

def printc(request,id):
    pr = Product.objects.get(id=id)
    data =('http://192.168.137.101:8000/product_details/'+id)
    img = make(data)
    img_name = 'qr' + str(random.gauss(mu=0, sigma=1) ) + '.png'
    img.save(settings.MEDIA_ROOT + '/' + img_name)
    print={"print":pr,'img':img_name}
    return render(request ,"html/print.html",print)

def p_details(request,id):
    details = Product.objects.get(id=id)
    return render(request,"html/product_details.html",{"details":details})

