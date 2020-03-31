from django.db import models
from django.conf import settings
from blogapp.models import Post
from django.db.models.signals import pre_save, post_save, m2m_changed

# Create your models here.


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            cart_obj = qs.first()
            new_obj = False
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        request.session['cart_count'] = cart_obj.post.count()
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    post        = models.ManyToManyField(Post, blank=True)
    total       = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    subtotal    = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    fee         = models.DecimalField(max_digits=20, decimal_places=2, default=10.00)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    objects     = CartManager()

def __str__(self):
    return str(self.id)


def m2m_changed_cart_reciver(sender, instance, action, *args, **kwargs):
    posts = instance.post.all()
    total = 0
    for x in posts:
        total += x.price
    if instance.subtotal != total:
        instance.subtotal = total 
        instance.save()

m2m_changed.connect(m2m_changed_cart_reciver, sender=Cart.post.through)


def pre_save_cart_reciver(sender, instance, *args, **kwargs):
    instance.total = instance.subtotal + instance.fee

pre_save.connect(pre_save_cart_reciver, sender=Cart)