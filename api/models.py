from datetime import datetime
from django.contrib.gis.db import models
from django.contrib.auth.models import User

class ShopKeeper(models.Model):

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100,default="",blank=True,null=True)
    lat = models.CharField(max_length=100,default="",blank=True,null=True)
    lon = models.CharField(max_length=100,default="",blank=True,null=True)
    password = models.CharField(max_length=100,blank=True,null=True)

    shop_name = models.CharField(max_length=100,blank=True,null=True)
    #document nit,cedula
    document = models.BigIntegerField(default=0)
    #delivery_cost se usa
    delivery_cost = models.FloatField(default=2000)
    #delivery_time deleted
    delivery_time = models.IntegerField(default=10)
    image = models.ImageField(upload_to="shopkeepers",blank=True,null=True)
    point = models.PointField(srid=4326,default='POINT(4.673498 -74.063333)')
    #
    store_code = models.BigIntegerField(default=0)
    username  = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    telephone = models.CharField(max_length=100,blank=True,null=True)
    square_range = models.IntegerField(default=10)
    credit_card = models.BooleanField(blank=True,default=False)
    min_delivery_price = models.FloatField(default=5000)
    
    #0 = Colombia; 1= RD
    type = models.IntegerField(default=0)
    #shop_id
    shop_id = models.BigIntegerField(default=0)
    device = models.TextField(blank=True,null=True)
    open = models.BooleanField(blank=True,default=False)
    last_active = models.DateTimeField(default=datetime.now, blank=True)
    rate = models.FloatField(default=0)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="categories",blank=True,null=True)
    def __unicode__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    subcategory = models.ForeignKey(Subcategory,blank=True,null=True)
    type = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

class Inventory(models.Model):
    shopkeeper = models.ForeignKey(ShopKeeper)
    product = models.ForeignKey(Product)
    price = models.FloatField(default=0,blank=True,null=True)

    def save(self, *args, **kwargs):

        if not self.price:
            self.price = self.product.price
        super(Inventory, self).save(*args, **kwargs)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(blank=True,null=True)
    device = models.TextField(blank=True,null=True)
    device_type = models.TextField(blank=True,null=True,default="android")
    telephone = models.CharField(max_length=15,blank=True,null=True)

    #0== App, 1== Telefono
    type = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name + " " + self.lastname


class Address(models.Model):
    address = models.CharField(max_length=100)
    address_detail = models.CharField(max_length=100,blank=True,null=True)
    type = models.IntegerField(default=0)
    client = models.ForeignKey(Client)

    def __unicode__(self):
        return self.address


class Moteros(models.Model):

    #Shopkeeper para quien trabaja
    #boss = models.ForeignKey(ShopKeeper,blank=True,null=True)
    name = models.CharField(max_length=64)
    plate = models.CharField(max_length=16)
    #Off Duty 0, On Duty 1
    #duty = models.BooleanField(blank=True,default=False)
    #Como trabaja, 0 paga despues de entregar domicilio, 1 paga antes o 2 paga cuando hace todos los domicilios
    #Pagar TODO boton

    type = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name + " - " + self.plate

class Rating(models.Model):
    shopkeeper = models.ForeignKey(ShopKeeper)
    client = models.ForeignKey(Client)
    rating = models.IntegerField()
    comment = models.TextField()

class Order(models.Model):

    products = models.ManyToManyField(Product, through='OrderProducts')
    client = models.ForeignKey(Client)
    state = models.IntegerField(default=0)
    shopkeeper = models.ForeignKey(ShopKeeper,blank=True,null=True)
    address = models.ForeignKey(Address,blank=True,null=True)
    motero = models.ForeignKey(Moteros,blank=True,null=True)
    total = models.FloatField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)
    type = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    comments = models.TextField(blank=True,null=True)
    payment  = models.IntegerField(default=0)
    delivery_cost = models.IntegerField(default=0)
    notified = models.BooleanField(blank=True,default=False)
    rating = models.OneToOneField(
        Rating,
        on_delete=models.CASCADE,
        blank=True,
        null=True

    )
    def __unicode__(self):
        return self.client.name + " " + self.client.lastname



class OrderProducts(models.Model):

    Product = models.ForeignKey(Product)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)

    def __unicode__(self):
        return self.Product.name + " - " + str(self.Quantity)

