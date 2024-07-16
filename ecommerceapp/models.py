from django.db import models

# Create your models here.
class ecomregister(models.Model):
    propic=models.ImageField(upload_to="images/")
    fullname=models.CharField(max_length=100)
    email=models.CharField(max_length=200)
    phone=models.IntegerField()
    gender=models.CharField(max_length=10)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.fullname


class sellerproduct(models.Model):
    productimage=models.ImageField(upload_to="images/")
    product=models.CharField(max_length=200)
    category=models.CharField(max_length=20)
    price=models.IntegerField()
    size=models.CharField(max_length=200)
    desc=models.CharField(max_length=500)
    def __str__(self):
        return self.product


class cartitem(models.Model):
    userid=models.IntegerField()
    item=models.ForeignKey(sellerproduct,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    selectedsize=models.CharField(max_length=10)


class wishlist(models.Model):
    userid=models.IntegerField()
    item=models.ForeignKey(sellerproduct,on_delete=models.CASCADE)


class addressdetails(models.Model):
    userid=models.ForeignKey(ecomregister,on_delete=models.CASCADE)
    address_line1=models.CharField(max_length=200)
    address_line2=models.CharField(max_length=200)
    pincode=models.IntegerField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    contact_name=models.CharField(max_length=100)
    contact_number=models.IntegerField()


class Order(models.Model):
    userdetails=models.ForeignKey(ecomregister,on_delete=models.CASCADE)
    address=models.ForeignKey(addressdetails,on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_now_add=True)


class orderitem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    order_pic=models.ImageField()
    pro_name=models.CharField(max_length=20)
    quantity=models.IntegerField()
    price=models.IntegerField()
    order_status=models.BooleanField(default=True)
# here order model has no connection with cart model





