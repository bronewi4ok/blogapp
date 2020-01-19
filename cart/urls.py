from django.urls import path, include
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('update', views.cart_update, name='cart_update')
]