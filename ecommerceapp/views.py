from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.conf import settings
import stripe
from django.core.mail import send_mail
from datetime import datetime,timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages

# Create your views here.
def registration(request):
    if(request.method=="POST"):
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        propic=request.FILES.get('propic')
        gender=request.POST.get("gender")
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')

        if(password==cpassword):
            data=ecomregister(fullname=fullname,email=email,phone=phone,propic=propic,gender=gender,password=password)
            data.save()
            return redirect(userlogin)
        else:
            return HttpResponse('registration failed')

    return render(request,'registration.html')



def userlogin(request):
    if(request.method=="POST"):
        email=request.POST.get('email')
        password=request.POST.get('password')
        data=ecomregister.objects.all()
        for i in data:
            if(i.email==email and i.password==password):
                request.session['userid']=i.id
                return redirect(userprofile)
        else:
            return HttpResponse('login failed')
    return render(request,'userlogin.html')


def userprofile(request):
    try:
        id1=request.session['userid']
        data=ecomregister.objects.get(id=id1)

        category = request.GET.get('category','all') # get selected category,if there is no category selected, all option will work
        if category=='all':
            db=sellerproduct.objects.all()
        else:
            db=sellerproduct.objects.filter(category=category)
        for item in db:
            item.size=item.size.split(',')
    except KeyError:
        return redirect(userlogin)

    return render(request,'userprofile.html',{'data':data,'db':db})



def updateprofile(request,id):
    data=ecomregister.objects.get(id=id)
    if(request.method=="POST"):
        if(request.FILES.get('propic')==None):
            data.save()
        else:
            data.propic=request.FILES.get('propic')
        data.fullname=request.POST.get('fullname')
        data.email=request.POST.get('email')
        data.phone=request.POST.get('phone')
        data.gender=request.POST.get('gender')
        data.save()
        return redirect(userprofile)

    return render(request,'updateprofile.html',{'data':data})


# def sellerproductupload(request):
#     if(request.method=='POST'):
#         category=request.POST.get('category')
#         productimage=request.FILES.get('productimage')
#         product=request.POST.get('product')
#         price=request.POST.get('price')
#         size=request.POST.get('size')
#         desc=request.POST.get('desc')
#         data=sellerproduct(category=category,productimage=productimage,product=product,price=price,size=size,desc=desc)
#         data.save()
#         return HttpResponse("upload successfully")
#     return render(request,"sellerproductupload.html")


def addtocart(request,itemid):
    item=sellerproduct.objects.get(id=itemid)
    cart=cartitem.objects.all()
    size=''
    if(request.method=='GET'):
        size=request.GET.get('size')
    for i in cart:
        if i.item.id==itemid and i.selectedsize==size and i.userid==request.session['userid']:
            i.quantity+=1
            i.save()
            return redirect(cartdisplay)
    else:
        db=cartitem(userid=request.session['userid'],item=item,selectedsize=size)
        db.save()
        return redirect(cartdisplay)


def cartdisplay(request):
    userid=request.session['userid']
    db=cartitem.objects.filter(userid=userid)
    total=0
    count=0
    for i in db:
        i.item.price*=i.quantity
        total+=i.item.price
        count+=1
    return render(request,'cartdisplay.html',{'db':db,'total':total,'count':count})


def inc_dec(request,cartid):
    db=cartitem.objects.get(id=cartid)
    action=request.GET.get('action')
    if action=='increment':
        db.quantity+=1
        db.save()
    elif action=='decrement' and db.quantity>1:
        db.quantity-=1
        db.save()
    return redirect(cartdisplay)

def removecart(request,cartid):
    db=cartitem.objects.get(id=cartid)
    db.delete()
    return redirect(cartdisplay)

def wishlistproduct(request,itemid):
    item=sellerproduct.objects.get(id=itemid)
    cart=wishlist.objects.all()
    for i in cart:
        if i.item.id==itemid and i.userid==request.session['userid']:
            return redirect(wishlistdisplay)
    else:
        db=wishlist(userid=request.session['userid'],item=item)
        db.save()
        return redirect(wishlistdisplay)


def wishlistdisplay(request):
    userid = request.session['userid']
    db = wishlist.objects.filter(userid=userid)
    for i in db:
        i.item.size = i.item.size.split(',')
    return render(request,"wishlistdisplay.html",{'db':db})

def removewishlist(request,itemid):
    db=wishlist.objects.get(id=itemid)
    db.delete()
    return redirect(wishlistdisplay)

def wishtoadd(request,itemid):
    item =sellerproduct.objects.get(id=itemid)
    cart = cartitem.objects.all()
    size = ''
    if (request.method == 'GET'):
        size = request.GET.get('size')
    for i in cart:
        if i.item.id == itemid and i.selectedsize == size and i.userid == request.session['userid']:
            i.quantity += 1
            i.save()
            return redirect(cartdisplay)
    else:
        db = cartitem(userid=request.session['userid'], item=item, selectedsize=size)
        db.save()
        return redirect(cartdisplay)


def address(request):
    id1=request.session['userid']
    data=ecomregister.objects.get(id=id1)
    if (request.method=='POST'):
        address_line1=request.POST.get('address_line1')
        address_line2=request.POST.get('address_line2')
        pincode=request.POST.get('pincode')
        city=request.POST.get('city')
        state=request.POST.get('state')
        contact_name=request.POST.get('contact_name')
        contact_number=request.POST.get('contact_number')
        db=addressdetails(userid=data,address_line1=address_line1,address_line2=address_line2,pincode=pincode,city=city,state=state,contact_name=contact_name,contact_number=contact_number)
        db.save()
        return redirect(delivery_details)
    return render(request,'addressadd.html')



def delivery_details(request):
    id=request.session['userid']
    data=addressdetails.objects.filter(userid__id=id)
    return render(request,'deliveryaddress.html',{'data':data})

def summary(request):
    userid=request.session['userid']
    address_id=request.GET.get('address')
    address=addressdetails.objects.get(id=address_id)
    cartitems=cartitem.objects.filter(userid=userid)

    key=settings.STRIPE_PUBLISHABLE_KEY
    striptotal=0
    total=0
    for i in cartitems:
        total+=i.item.price
        striptotal=total*100
    expected_delivery_date = datetime.now() + timedelta(days=7)


    return render(request,'summary.html',{'address':address,'cartitems':cartitems,'total':total,'key':key,'striptotal':striptotal,'expected_delivery_date':expected_delivery_date.strftime('%Y-%m-%d')})


def createorder(request):
    if request.method=="POST":
        order_items=[]
        total_price=0
        userid=request.session['userid']
        user=ecomregister.objects.get(id=userid)
        address_id=request.POST.get('address_id')
        address=addressdetails.objects.get(id=address_id)
        cart=cartitem.objects.filter(userid=userid)

        order=Order.objects.create(userdetails=user,address=address)
        for i in cart:
            orderitem.objects.create(order=order,order_pic=i.item.productimage,pro_name=i.item.product,quantity=i.quantity,price=i.item.price)

            total_price+=i.item.price*i.quantity

            order_items.append({'product':i.item.product,'quantity':i.quantity,'price':i.item.price*i.quantity})  #mail lekku
        expected_delivery_date=datetime.now()+timedelta(days=7)

        subject='Order conformation'
        context={'order_items':order_items,'total_price':total_price,'expected_delivery_date':expected_delivery_date.strftime('%Y-%m-%d')}
        html_message=render_to_string('order_confirmation_email.html',context)

        plain_message=strip_tags(html_message)

        from_email='mssusmitha.007@gmail.com'
        to_email=[user.email]
        send_mail(subject,plain_message,from_email,to_email,html_message=html_message)
        cart.delete()
        return HttpResponse('order created successfully')


def ordereditems(request):
    userid=request.session['userid']
    order=orderitem.objects.filter(order__userdetails__id=userid).order_by('-order__ordered_date')
    return render(request,'order.html',{'order':order})


def cancelorder(request,orderid):
    data=orderitem.objects.get(id=orderid)
    data.order_status=False
    data.save()
    userid = request.session['userid']
    user = ecomregister.objects.get(id=userid)

    subject = 'Order cancelation'
    context = {'cancel_item': data.pro_name, 'price': data.price
               }
    html_message = render_to_string('order_cancellation_email.html', context)

    plain_message = strip_tags(html_message)

    from_email = 'mssusmitha.007@gmail.com'
    to_email = [user.email]
    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

    return HttpResponse('Order cancelled')
def changepassword(request):
    id1=request.session['userid']
    db=ecomregister.objects.get(id=id1)
    if(request.method=='POST'):
        oldpassword=request.POST.get('old')
        if db.password==oldpassword:
            newpassword=request.POST.get('new')
            retypepassword=request.POST.get('retype')
            if(newpassword==retypepassword):
                db.password=newpassword
                db.save()
                return redirect(userlogin)
            else:
                messages.error(request, 'Password dont match')
        else:
            messages.error(request, 'please enter correct password')




    return render(request,'passwordchange.html')



def logout(request):
    request.session.flush()
    return redirect(index)


def forgotpass(request):
    data=ecomregister.objects.all()
    if request.method=='POST':
        email=request.POST.get('email')
        for i in data:
            if i.email==email:
                subject = 'change password'

                html_message = render_to_string('passwordmail.html',{'email':i.email,'id':i.id})

                plain_message = strip_tags(html_message)

                from_email = 'mssusmitha.007@gmail.com'
                to_email = [i.email]
                send_mail(subject, plain_message, from_email, to_email, html_message=html_message)


                return redirect(renewpassword)
            else:
                messages.error(request, 'please enter correct Email')
    return render(request,'forgotpassword.html')





def renewpassword(request,id):

    if request.method=="POST":
        data=ecomregister.objects.get(id=id)
        password=request.POST.get('pass')
        cpassword=request.POST.get('repass')
        if password==cpassword:
            data.password=password
            data.save()
            return redirect(userlogin)
        else:
            messages.error(request, 'please enter correct password')



    return render(request,'correctpassword.html')
























def index(request):
    return render(request,'index.html')