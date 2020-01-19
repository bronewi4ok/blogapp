from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from cart.models import Cart
from mysite.utils import unique_order_id_generator
import math
from decimal import Decimal
# Create your models here.


ORDER_STATUS_CHOISES = {
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('hipped', 'Shipped'),
    ('refaunded', 'Refaunded'),
}

class Order(models.Model):
    order_id        = models.CharField( max_length=120, blank=True)
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status          = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOISES)
    shipping_total  = models.DecimalField(max_digits=100, decimal_places=2, default=5.99)
    total           = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = Decimal(cart_total) + Decimal(shipping_total)
        self.total = new_total
        self.save()
        return new_total


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
                cart_obj = qs.first()
                cart_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)
