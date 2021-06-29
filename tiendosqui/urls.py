"""tiendosqui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from api import views
urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^order/', views.order, name='order'),
    url(r'^order_servi/', views.order_servi, name='order_servi'),
    url(r'^order-detail/(?P<order_id>[0-9]+)/$', views.order_detail, name='order_detail'),
    url(r'^confirm/', views.confirm, name='confirm'),
    url(r'^reject/', views.reject, name='reject'),
    url(r'^shopkeepers/', views.shopkeepers_list, name='shopkeepers_list'),
    url(r'^inventory/', views.inventory, name='inventory'),
    url(r'^deliveries/', views.deliveries, name='deliveries'),
    url(r'^user/', views.user_add, name='user_add'),
    url(r'^shopkeeper_add/', views.shopkeeper_add, name='shopkeeper_add'),
    url(r'^client/login/$', views.client_login, name='client_login'),
    url(r'^address/', views.address, name='address'),
    url(r'^push/', views.push, name='push'),
    url(r'^login/', views.shopkeeper_login, name='login'),
    url(r'^open/', views.open, name='open'),
    url(r'^credit_card/', views.credit_card, name='credit_card'),
    url(r'^notified/', views.notified, name='notified'),
    url(r'^update_cost_delivery/', views.delivery_cost, name='delivery_cost'),
    url(r'^pedido/$', views.delivery, name='delivery'),
    url(r'^online/$', views.online, name='online'),
    url(r'^rate/$', views.rate, name='rate'),
    url(r'^get_ratings/$', views.get_ratings, name='get_ratings'),
    url(r'^order_detail_json/$', views.order_detail_json, name='order_detail_json'),
    url(r'^shopkeepers_state/$', views.shopkeepers_state, name='shopkeepers_state'),
    url(r'^shopkeepers_admin/$', views.shopkeepers_admin, name='shopkeepers_admin'),
    url(r'^push_test/$', views.push_test, name='push_test'),

    url(r'^categories/$', views.categories, name='categories'),
    url(r'^category/products/$', views.category_products, name='category_products'),
    url(r'^set_inventory/$', views.set_inventory, name='set_inventory'),
    url(r'^$', views.index, name='index'),

]
