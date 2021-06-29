import json
import random
import string
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.http import HttpResponse
from django.contrib.gis.measure import D, Distance
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from push_notifications.apns import apns_send_message
from push_notifications.gcm import gcm_send_message
import requests
from api.models import ShopKeeper, Inventory, Client, Address, Order, Product, OrderProducts, Rating, Category, Moteros
from django.http import JsonResponse
from push_notifications.models import GCMDevice, APNSDevice
from django.core.validators import validate_email
from datetime import datetime
from django.contrib.auth import authenticate, login

def index(request):
    filter = request.GET.get('state')
    if filter is None:
        orders = Order.objects.all().order_by("-id")
    else:
        orders = Order.objects.filter(state=filter).order_by("-id")

    context = {"orders":orders}
    return render(request, 'index.html', context)


def shopkeepers_admin(request):

    shopkeepers = ShopKeeper.objects.all().order_by("-last_active")
    context = {"shopkeepers":shopkeepers}

    return render(request, 'shopkeepers.html', context)

@csrf_exempt
def shopkeepers_state(request):
    if request.method == "POST":
        shopkeepers = ShopKeeper.objects.all()

        data = []
        for s in shopkeepers:
            data.append({"id": s.id,"last_active":s.last_active,"open":s.open})

        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))



def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    context = {"order":order}
    return render(request, 'order.html', context)

@csrf_exempt
def order_detail_json(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = Order.objects.get(pk=order_id)
        return JsonResponse({"client":order.client.name + " "+order.client.lastname,"id":order.id,"shopkeeper_id":order.shopkeeper.id,"shopkeeper":order.shopkeeper.name,"address":order.address.address,"state":order.state,"notified":order.notified,"date":order.date })

@csrf_exempt
def settings(request):
    """
    Lista de tenderos dada una coordenada
    :param request, point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """
    if request.method == "POST":

        delivery_cost = request.POST.get("delivery_cost")
        minimum_delivery = request.POST.get("minimum_delivery")

@csrf_exempt
def shopkeepers_list(request):
    """
    
    Lista de tenderos dada una coordenada
    :param request, point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """
    if request.method == "POST":

        point = request.POST.get("point")
        point = GEOSGeometry(point, srid=4326)

        result = ShopKeeper.objects\
            .filter(point__distance_lte=(point, D(km=1110)))\
            .annotate(num_orders=Count('order'))\
            .values('name','num_orders','lat','lon','shop_name','delivery_cost','id','open','image','rate','telephone','address', 'delivery_time','square_range', 'credit_card','min_delivery_price')
        result = list(result)

        return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder))
    else:
        if request.method == "GET":

            point = 'POINT(-74.536610 4.719120)'
            point = GEOSGeometry(point, srid=4326)

            result = ShopKeeper.objects\
                .filter(point__distance_lte=(point, D(km=1110)))\
                .annotate(num_orders=Count('order'))\
                .values('name','num_orders','lat','lon','shop_name','delivery_cost','id','open','image','rate','telephone','address', 'delivery_time','square_range', 'credit_card','min_delivery_price')

            result = list(result)
            return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder))


@csrf_exempt
def inventory(request):

    """
    Lista de productos de un tendero
    :param request, point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """

    if request.method == "POST":
        id = request.POST.get("shopkeeper_id")

        shopkeeper = ShopKeeper.objects.get(pk=id)
        inventory = Inventory.objects.filter(shopkeeper=shopkeeper)
        data = []
        for i in inventory:
            data.append({
                'product_name':i.product.name,
                'product_id':i.product.id,
                'product_price':i.product.price,
                'custom_price':i.price,
                'subcategory_name':i.product.subcategory.name,
                'category_name':i.product.subcategory.category.name,
                'category_image':'http://api.tiendosqui.com/static/media/'+i.product.subcategory.category.image.url,
                'category_id':i.product.subcategory.category.id,
                'subcategory_id':i.product.subcategory.id,
            })

        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))

    else:
        if request.method == "GET":

            id = 1

            shopkeeper = ShopKeeper.objects.get(pk=id)
            inventory = Inventory.objects.filter(shopkeeper=shopkeeper)
            data = []
            for i in inventory:
                data.append({
                    'product_name':i.product.name,
                    'product_id':i.product.id,
                    'product_price':i.product.price,
                    'custom_price':i.price,
                    'subcategory_name':i.product.subcategory.name,
                    'category_name':i.product.subcategory.category.name,
                    'category_image':'http://api.tiendosqui.com/static/media/'+i.product.subcategory.category.image.url,
                    'category_id':i.product.subcategory.category.id,
                    'subcategory_id':i.product.subcategory.id,
                })

            return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))


@csrf_exempt
def deliveries(request):

    """
    Lista de productos de un tendero
    :param request, point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """


    id = request.POST.get("shopkeeper_id")

    shopkeeper = ShopKeeper.objects.get(pk=id)
    orders = Order.objects.all().filter(shopkeeper=shopkeeper).order_by('-id')[:20]
    data = []
    for i in orders:

        products = i.orderproducts_set.all()
        products_a = []

        for p in products:

            products_a.append({
                "name": p.Product.name,
                "count": p.Quantity,
                "unit_price": p.Product.price
            })


        if(i.type == 0):
            title = "Pedido por Don Colmado"
        else:
            title = "Pedido por Telefono"

        data.append({
            "title": title,
            'state':i.state,
            "order_id":i.id,
            "date": i.date.replace(microsecond=0,tzinfo=None),
            'products': products_a,
            "address": i.address.address,
            "client_name": i.client.name+" "+i.client.lastname,
            "client_telephone": i.client.telephone,
            "address_details": i.address.address_detail,
            "comments": i.comments,
            "payment": i.payment,
            "delivery_cost": i.delivery_cost
        })

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder,indent=4,separators=(',', ': ')), content_type='application/json')


@csrf_exempt
def user_add(request):
    """
    Lista de tenderos dada una coordenada
    :param request, 0point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """
    if request.method == "POST":

        name = request.POST.get("name")
        lastname = request.POST.get("lastname")
        password = request.POST.get("password")
        telephone = request.POST.get("telephone")
        email = request.POST.get("email")
        device = request.POST.get("device")
        device_type = request.POST.get("device_type")
        try:
            Client.objects.get(email=email)
            return HttpResponse("error")
        except:

            username = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
            user = User.objects.create_user(username, email, password)
            client = Client(user=user,name=name,lastname=lastname,email=email,device=device,telephone=telephone,device_type=device_type)
            client.save()

            if device_type == "ios":
                apn = APNSDevice(registration_id=device)
                apn.save()
            else:

                gcm = GCMDevice(registration_id=device)
                gcm.save()

            return JsonResponse({'client':client.id})


@csrf_exempt
def shopkeeper_add(request):
    """
    Cread un nuevo shopkeeper
    :param request, 0point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """
    if request.method == "POST":

        name = request.POST.get("name")
        address = request.POST.get("address")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")
        password = request.POST.get("password")
        shop_name = request.POST.get("shop_name")
        delivery_cost = request.POST.get("delivery_cost")
        username = request.POST.get("username")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        square_range = request.POST.get("square_range")
        device = request.POST.get("device")
        try:
            ShopKeeper.objects.get(email=email)
            return JsonResponse({'status':1,"message":"Invalid email."})
        except:

            #username = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
            shopkeeper = ShopKeeper(name=name,address=address,email=email,lat=lat,lon=lon,password=password,shop_name=shop_name,delivery_cost=delivery_cost,username=username,telephone=telephone,square_range=square_range,device=device)
            shopkeeper.save()

            gcm = GCMDevice(registration_id=device)
            gcm.save()

            return JsonResponse({'status':"0","name":shopkeeper.name,"email":shopkeeper.email,"username":shopkeeper.username,"profile_id":shopkeeper.id,"shop_id":shopkeeper.shop_id,
                                     "telephone":shopkeeper.telephone})         


@csrf_exempt
def shopkeeper_login(request):

    """
    Lista de tenderos dada una coordenada
    :param request, 0point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """

    if request.method == "POST":
        username   = request.POST.get("username")
        password   = request.POST.get("password")
        device = request.POST.get("device",None)
        #email = False
        email = True
        #try:
        #    validate_email(username)
        #    email = True

        #except ValidationError as e:
        #   email = False


        if(email):
            try:
                shopkeeper = ShopKeeper.objects.get(username=username,password=password)
                if device != None:
                    shopkeeper.device = device
                    shopkeeper.save()
                    gcm = GCMDevice(registration_id=device)
                    gcm.save()
                return JsonResponse({'status':"0","name":shopkeeper.name,"email":shopkeeper.email,"username":shopkeeper.username,"profile_id":shopkeeper.id,"shop_id":shopkeeper.shop_id,
                                     "telephone":shopkeeper.telephone})
            except:
                 return JsonResponse({'status':1,"message":"Invalid password."})

        payload = {'username': username, 'password': password}
        try:
            shopkeeper = ShopKeeper.objects.get(username=username)
            #Ya esta registrado
            r = requests.post("http://servi-test-saphety.appspot.com/login", data=json.dumps(payload))
            r = r.json()

            status =  r["status"]
            message = r["message"]

            if(status == 0):
                if device != None:
                    shopkeeper.device = device
                    shopkeeper.save()
                    gcm = GCMDevice(registration_id=device)
                    gcm.save()
                return JsonResponse({'status':"0","name":shopkeeper.name,"email":shopkeeper.email,"username":shopkeeper.username,"profile_id":shopkeeper.id,"shop_id":shopkeeper.shop_id,
                                     "telephone":shopkeeper.telephone})

            else:
                return JsonResponse({'status':status,"message":message})

        except:

            r = requests.post("http://servi-test-saphety.appspot.com/login", data=json.dumps(payload))
            r = r.json()

            status = r["status"]
            message = r["message"]
            if(status == 0):

                user       = r["user"]
                profile_id = user["profile_id"]
                email       = user["email"]
                username = user["username"]
                cedula_document = user["cedula_document"]
                store_code = user["store_code"]
                contact = r["contact information"][0]
                owner_name = contact["owner_name"]
                store_name = contact["store_name"]
                address = contact["address"]
                lat = contact["latitude"]
                lon = contact["altitude"]
                telephone = contact["telephone"]

                point = 'POINT('+lon+' '+lat+')'
                point = GEOSGeometry(point, srid=4326)
                shopkeeper = ShopKeeper(name=owner_name,shop_name=store_name,
                                        address=address,email=email,username=username,
                                        document=cedula_document,point=point,store_code=store_code,lat=lat,lon=lon,shop_id=profile_id,telephone=telephone)
                shopkeeper.save()
                if device != None:
                    shopkeeper.device = device
                    shopkeeper.save()
                    gcm = GCMDevice(registration_id=device)
                    gcm.save()

                return JsonResponse({'status':"0","name":shopkeeper.name,
                                     "email":shopkeeper.email,
                                     "username":shopkeeper.username,
                                     "profile_id":shopkeeper.id,
                                     "shop_id":shopkeeper.shop_id,
                                     "telephone":shopkeeper.telephone})
            else:
                return JsonResponse({'status':status,"message":message})
            return HttpResponse(r["status"])

@csrf_exempt
def address(request):

    if request.method == "POST":

        address   = request.POST.get("address")
        address_detail = request.POST.get("address_detail")
        client_id = request.POST.get("client")
        client = Client.objects.get(pk=client_id)
        address =  Address(address=address,address_detail=address_detail,client=client,type=0)
        address.save()
        return JsonResponse({'address':address.id})

@csrf_exempt
def open(request):

    if request.method == "POST":

        open   = request.POST.get("open")
        shopkeeper_id = request.POST.get("shopkeeper_id")
        shopkeeper = ShopKeeper.objects.get(pk=shopkeeper_id)
        if(open == "0"):
            result = bool(False)
        else:
            result = bool(True)
        shopkeeper.open = result
        shopkeeper.save()

        return JsonResponse({'open':result})
@csrf_exempt
def credit_card(request):

    if request.method == "POST":

        credit_card = request.POST.get("credit_card")
        shopkeeper_id = request.POST.get("shopkeeper_id")
        shopkeeper = ShopKeeper.objects.get(pk=shopkeeper_id)
        if(credit_card == "0"):
            result = bool(False)
        else:
            result = bool(True)
        shopkeeper.credit_card = result
        shopkeeper.save()

        return JsonResponse({'credit_card':result})

@csrf_exempt
def notified(request):

    if request.method == "POST":

        order_id   = request.POST.get("order_id")
        order = Order.objects.get(pk=order_id)

        result = bool(True)
        order.notified = result
        order.save()

        return JsonResponse({'order':result})

@csrf_exempt
def delivery_cost(request):

    if request.method == "POST":

        delivery_cost   = request.POST.get("delivery_cost")
        shopkeeper_id = request.POST.get("shopkeeper_id")
        shopkeeper = ShopKeeper.objects.get(pk=shopkeeper_id)

        shopkeeper.delivery_cost = delivery_cost
        shopkeeper.save()

        return JsonResponse({'delivery_cost':shopkeeper.delivery_cost})

@csrf_exempt
def order(request):
    """
    Lista de tenderos dada una coordenada
    :param request, point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """
    if request.method == "POST":
        order  = json.loads(request.POST.get("order"))

        client_id = Client.objects.get(pk=int(order["client"]))
        shopkeeper = ShopKeeper.objects.get(pk=order["shopkeeper"])
        address = Address.objects.get(pk=order["address"])
        comments = order["comments"]
        payment = order["payment"]
        delivery_cost = order["delivery_cost"]
        new_order = Order(client=client_id,shopkeeper=shopkeeper,address=address,total=order["total"],comments=comments,payment=payment,delivery_cost=delivery_cost)
        new_order.save()
        for key, value in order["products"].iteritems():

            product = Product.objects.get(pk=order["products"][key]["id"])
            po = OrderProducts(Product=product,Order=new_order,Quantity=order["products"][key]["count"])
            po.save()

        new_order.save()
        data = {
            'title': 'Tiendosqui',
            'body': 'Nuevo pedido',
            'id':"1",
            'order_id':str(new_order.id),
            'message':"Nuevo pedido",
        }

        gcm_send_message(shopkeeper.device, data)
        return JsonResponse({'result':new_order.id,'shopkeeper_id':shopkeeper.device})

@csrf_exempt
def push_test(request):
    """
    Lista de tenderos dada una coordenada
    :param request, point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """
    if request.method == "POST":
        device_id  = "dHZaauu2Jgc:APA91bGYiV6Nsb7-A1YjcdFWNySH9HU7pRqyAbS4amCns8a-oQiI6pLUvZOao161P-OF778zsj6zexxZKOCmOyLYwon8POk63CWGyNeg03MKxcKLre_GAMoNUUDmGlmlRxKdRkJfGfkx"
        data = {
            'title': 'Tiendosqui',
            'body': 'Nuevo pedido',
            'id':"1",
            'order_id':9999,
            'message':"Nuevo pedido",
        }
        gcm_send_message(device_id, data)
        
        return HttpResponse("Success notification?.")

@csrf_exempt
def rate(request):
    if request.method == "POST":

        shopkeeper_id = request.POST.get("shopkeeper_id")
        client_id = request.POST.get("client_id")
        order_id = request.POST.get("order_id")
        comment  = request.POST.get("comment")
        rating  = request.POST.get("rating")


        client = Client.objects.get(pk=client_id)
        shopkeeper = ShopKeeper.objects.get(pk=shopkeeper_id)
        order = Order.objects.get(pk=order_id)

        r = Rating(shopkeeper=shopkeeper,client=client,comment=comment,rating=rating)
        r.save()

        order.rating = r
        order.save()

        number = Rating.objects.filter(shopkeeper=shopkeeper).count()

        shopkeeper.rate = (shopkeeper.rate+float(rating))/number
        shopkeeper.save()



        return JsonResponse({'result':r.id})


@csrf_exempt
def order_servi(request):
    """
    :param request, with order
    :return httpresponse
    """
    if request.method == "POST":
        order  = json.loads(request.POST.get("order"))
        # Datos de client para verificar si ya existe
        client_emailEx = order["client"]["email"]
        # Reviso que no este creado si lo esta debo traerlo por el ID
        try:
            clientEx = Client.objects.get(email=client_emailEx)
            client = clientEx
            client_id = client.id
        except:
            #Si no existe crearlo y agarrar el ID
            client = order["client"]
            client_name = client["name"]
            client_lastname = client["lastname"]
            client_password = client["password"]
            client_telephone = client["telephone"]
            client_email = client["email"]
            client_device = "ServiPunto"

            client_username = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
            client_user = User.objects.create_user(client_username, client_email, client_password)

            client = Client(user=client_user, name=client_name, lastname=client_lastname, email=client_email, device=client_device, telephone=client_telephone)
            client.save()
            client_id = client.id

        # Datos de address
        address = order["address"]["address"]
        address_detail = order["address"]["address_detail"]
        address = Address(address=address, address_detail=address_detail,client=client)
        address.save()
        address_id = address.id

        ##############################################################
        shopkeeper = ShopKeeper.objects.get(pk=order["shopkeeper"])
        comments = order["comments"]
        payment = order["payment"]
        delivery_cost = order["delivery_cost"]
        new_order = Order(client=client,shopkeeper=shopkeeper,address=address,total=order["total"],comments=comments,payment=payment,delivery_cost=delivery_cost)
        new_order.save()
        for key, value in order["products"].iteritems():
            # Agarro el nombre y lo comparo para saber si ya existe
            product_nameEx = order["products"][key]["name"]
            try:
                productEx = Product.objects.get(name=product_nameEx)
                product = productEx
            except:
                # Datos de producto
                product =  order["products"][key]
                product_name = product["name"]
                product_price = product["price"]
                #product_subcat = product["subcategory"]
                product_type = 0
                product = Product(name=product_name, price=product_price, type=product_type)
                product.save()

            product_id = product.id
            po = OrderProducts(Product=product, Order=new_order, Quantity=order["products"][key]["count"])
            po.save()

        new_order.save()
        data = {
            'title': 'Tiendosqui',
            'body': 'Nuevo pedido desde ServiPunto',
            'id':"1",
            'order_id':str(new_order.id),
            'message':"Nuevo pedido desde ServiPunto",
        }

        gcm_send_message(shopkeeper.device, data)
        return JsonResponse({'orden_id':new_order.id,'status':'OK'})


@csrf_exempt
def delivery(request):
    """
    Delivery por telefono
    :param request, point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """
    if request.method == "POST":

        total       = 0
        data        = json.loads(request.body)
        tendero     = data["tendero"]
        store_code  = tendero["store_code"]
        shopkeeper  = ShopKeeper.objects.get(store_code=store_code)

        cliente = data["cliente"]
        cliente_nombre = cliente["nombre"]
        cliente_apellido = cliente["apellido"]
        cliente_direccion = cliente["direccion"]
        cliente_email = cliente["correo"]
        cliente_telefono = cliente["telefono"]

        if(cliente_email != ""):
            client = Client(name=cliente_nombre,lastname=cliente_apellido,type=1,telephone=cliente_telefono,email=cliente_email)
        else:
            client = Client(name=cliente_nombre,lastname=cliente_apellido,type=1,telephone=cliente_telefono)

        client.save()
        address = Address(address=cliente_direccion,client=client)
        address.save()



        pedido = data["pedido"]

        tiempo_entrega  = pedido["tiempo_entrega"]
        costo_envio = pedido["costo_envio"]
        comentarios = pedido["comentarios"]
        productos = pedido["productos"]

        for p in productos:

            p["cantidad"] = int(p["cantidad"])
            p["precio"] = float(p["precio"])
            total += (p["cantidad"]*p["precio"])


        order =  Order(client=client,shopkeeper=shopkeeper,address=address,total=total,time=tiempo_entrega,type=1,comments=comentarios)
        order.save()

        for p in productos:

            product = Product(name=p["nombre"],price=p["precio"],type=1)
            product.save()
            po = OrderProducts(Product=product,Order=order,Quantity=p["cantidad"])
            po.save()

        order.save()

        data = {
            'title': 'Tiendosqui',
            'body': 'Nuevo pedido',
            'id':"1",
            'message':"Nuevo pedido",
        }

        gcm_send_message('fgHQGZ5i9go:APA91bF95pXpXIZmRPXfuKIR9hG7zN3lCdUwrV3P3JT_pqh4PKMPlwdf_FoBqPjIHHF6LnIwhMcDAiipxbWxAjTRoWE9IN750UOKcHAFfzlqx8tB_Hj1t_USUI-tPPCGBc25blhEWtb3', data)

        return JsonResponse({'result':order.id})
    else:
        return HttpResponse("Invalid method.")


@csrf_exempt
def confirm(request):

    if request.method == "POST":

        order_id = request.POST.get("order_id")
        time = request.POST.get("time")

        try:
            order = Order.objects.get(pk=order_id)
        except:
            return HttpResponse(str(order_id)+" No existe")

        order.state = "1"
        order.notified = bool(True)
        order.time = time
        order.save()
       
        device = order.client.device

        data = {
            'title': 'Tiendosqui',
            'body': 'Tu pedido ha sido confirmado',
            'id':"1",
            'time':time,
            'device': device,
            'order': order_id,
        }
        if order.client.device_type == "ios":
            apns_send_message(device,data)
            return HttpResponse("ios")
        else:
            gcm_send_message(device, data)
        
        return HttpResponse("Success!")

    return HttpResponse("error!")


@csrf_exempt
def get_ratings(request):
    
    """
    Lista de calificaciones por tendero
    :param request, :id shopkeeper_id
    :return JSON(calificaciones)
    """

    if request.method == "POST":
        id = request.POST.get("shopkeeper_id")

        shopkeeper = ShopKeeper.objects.get(pk=id)
        ratings = Rating.objects.filter(shopkeeper=shopkeeper)
        data = []

        for i in ratings:
            data.append({
                'shopkeeper_id':i.shopkeeper.id,
                'client':i.client.name + " " + i.client.lastname,
                'rating':i.rating,
                'comment':i.comment,
            })

        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))


@csrf_exempt
def reject(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        message = request.POST.get("message")
        order = Order.objects.get(pk=order_id)

        order.state = "2"
        order.notified = bool(True)
        order.save()

        device = order.client.device

        data = {
            'title': 'Tiendosqui',
            'body': 'Tu pedido ha sido rechazado',
            'id':"2",
            'shopkeeper_message':message,
        }

        if order.client.device_type == "ios":
            apns_send_message(device,data)
        else:
            gcm_send_message(device, data)
        return HttpResponse("Success!")

@csrf_exempt
def online(request):

    if request.method == "POST":
        shopkeeper_id = request.POST.get("shopkeeper_id")
        shopkeeper = ShopKeeper.objects.get(pk=shopkeeper_id)
        shopkeeper.last_active = datetime.now()
        shopkeeper.save()
        return HttpResponse("success")


@csrf_exempt
def client_login(request):

    email = request.POST['email']
    password = request.POST['password']
    device = request.POST['device']
    device_type = request.POST['device_type']
    try:
        client = Client.objects.get(email=email)
    except:
         return JsonResponse({'status':"1"})
    client_user = client.user
    user = authenticate(username=client_user.username, password=password)
    if user is not None:
        if user.is_active:
            client.device = device
            client.device_type = device_type
            client.save()

            if device_type == "ios":
                apn = APNSDevice(registration_id=device)
                apn.save()
            else:

                gcm = GCMDevice(registration_id=device)
                gcm.save()
            return JsonResponse({'status':"0","name":client.name,
                                     "email":client.email,
                                     "lastname":client.lastname,
                                     "id":client.id})
        else:
            return JsonResponse({'status':"2"})

    else:
        return JsonResponse({'status':"3"})


def push(request):
    data = {
        'title': 'Tiendosqui',
        'body': 'Nuevo pedido',
        'id':"1",
        'message':"Nuevo pedido",
    }

    #device.send_message("Tu pedido ha sido confirmado")
    r = gcm_send_message('fEHhNNjNuX4:APA91bFyscyQf2ukZ9qO0xmQBzi7_HZyVnpIsUTIolPbs4pbF55lWAczaqoN7oKPAZxG_2RHDXmR6BzGIuFccQRqSs3w4iOSUeue_eCktJzRXV0MlbM4vydmP7wjiywjVw3wQ6L47qii', data)
    return HttpResponse(r)

"""
    Tablet tendero
"""

@csrf_exempt
def categories(request):

    """
    Lista de productos de un tendero
    :param request, point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """


    id = request.POST.get("shopkeeper_id")

    shopkeeper = ShopKeeper.objects.get(pk=id)
    categories = Category.objects.all()


    data = []

    for i in categories:
        data.append({
            'category_id':i.id,
            'name':i.name,
        })

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder,indent=4,separators=(',', ': ')), content_type='application/json')

@csrf_exempt
def category_products(request):

    """
    Lista de productos de un tendero
    :param request, point: POINT(-74.536610 4.719120):
    :return json(tenderos):
    """


    shopkeeper_id = request.POST.get("shopkeeper_id")
    category_id = request.POST.get("category_id")
    category = Category.objects.get(pk=category_id)
    shopkeeper = ShopKeeper.objects.get(pk=shopkeeper_id)
    products = Product.objects.filter(subcategory__category=category,type=0)
    inventory = Inventory.objects.filter(shopkeeper=shopkeeper).values_list('product__id', flat=True)
    prices = list(Inventory.objects.filter(shopkeeper=shopkeeper).values_list('price', flat=True))
    data = []

    for i in products:
        stock = bool(False)
        price = i.price

        if i.id in inventory:
            stock = bool(True)
            price = prices[list(inventory).index(i.id)]
        data.append({
            'product_id':i.id,
            'name':i.name,
            'price':price,
            'default_price':i.price,
            'category_id':i.subcategory.category.id,
            'stock': stock,
        })

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder,indent=4,separators=(',', ': ')), content_type='application/json')

@csrf_exempt
def set_inventory(request):

    if request.method == "POST":
        shopkeeper_id = request.POST.get("shopkeeper_id")
        product_id   = request.POST.get("product_id")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        product = Product.objects.get(pk=product_id)
        shopkeeper = ShopKeeper.objects.get(pk=shopkeeper_id)
        if(stock == "false"):
            stock = bool(False)
        else:
            stock = bool(True)

        if(stock):
            try:
                inventory = Inventory.objects.get(product=product,shopkeeper=shopkeeper)
                inventory.price = price
                inventory.save()
            except:
                inventory = Inventory(shopkeeper=shopkeeper,product=product,price=price)
                inventory.save()
        else:
            try:
                inventory = Inventory.objects.get(product=product,shopkeeper=shopkeeper)
                inventory.delete()
            except:
                pass


        return HttpResponse("success")
