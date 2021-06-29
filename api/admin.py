from django.contrib import admin
from push_notifications.models import GCMDevice

from .models import *

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ShopKeeper)
admin.site.register(Client)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Inventory)
admin.site.register(Subcategory)
admin.site.register(OrderProducts)
admin.site.register(Rating)
admin.site.register(Moteros)

