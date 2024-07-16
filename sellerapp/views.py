from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from ecommerceapp.models import *

# Create your views here.
def index(request):
    return render(request, 'sellerindex.html')

def register_seller(request):
    if request.method=='POST':
        form=SellerRegistrationForm(request.POST)
        #request.POST which is the method used to pass your POST data into your SellerRegistrationForm

        if form.is_valid():
            password=form.cleaned_data.get('password')
            cpassword=form.cleaned_data.get('cpassword')
            if password!=cpassword:
                messages.error(request,'Passord dont match')
            else:
                user=form.save(commit=False)
                user.set_password(password)
                user.save()
                messages.success(request,'Registration successful.you can now login.')
                return HttpResponse('Registration success')
    else:
        form=SellerRegistrationForm()

    return render(request,'register.html',{'form':form})


def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        #in django,AuthenticationFormis a builtin form class provided by the django.contrib.auth.form module
        #its designed to handle user authentication,particularly for logging users into web application
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')

            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                request.session['sellerid']=user.id
                messages.success(request,f'You are now logged in as{username}')
                #f is formatter(to read special characters)
                return redirect(profile_view)
            else:
                messages.error(request,'Invalid Username and Password')
        else:
            messages.error(request,'Form is not Valid')
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})

def profile_view(request):
    userid=request.session['sellerid']

    data=User.objects.get(id=userid)

    category = request.GET.get('category',
                               'all')  # get selected category,if there is no category selected, all option will work
    if category == 'all':
        cart = sellerproduct.objects.all()
    else:
        cart = sellerproduct.objects.filter(category=category)
    for item in cart:
        item.size = item.size.split(',')

    return render(request,'sellerprofile.html',{'data':data,'cart':cart})

# def index(request):
#     return render(request,'sellerindex.html')



def sellerproductupload(request):
    if(request.method=='POST'):
        category=request.POST.get('category')
        productimage=request.FILES.get('productimage')
        product=request.POST.get('product')
        price=request.POST.get('price')
        size=request.POST.get('size')
        desc=request.POST.get('desc')
        data=sellerproduct(category=category,productimage=productimage,product=product,price=price,
                           size=size,desc=desc)
        data.save()
        return HttpResponse("upload successfully")
    return render(request,"sellerproductupload.html")

def deleteitem(request,cartid):
    db=sellerproduct.objects.get(id=cartid)
    db.delete()
    return redirect(profile_view)

def edititem(request,cartid):
    data=sellerproduct.objects.get(id=cartid)
    if (request.method == "POST"):
        if (request.FILES.get('productimage') == None):
            data.save()
        else:
            data.productimage = request.FILES.get('productimage')
        data.category=request.POST.get('category')
        data.product = request.POST.get('product')
        data.price = request.POST.get('price')
        data.desc= request.POST.get('desc')
        data.size = request.POST.get('size')
        data.save()





