from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart
from blogapp.models import Post
from django.http import HttpResponseRedirect, JsonResponse
from orders.models import Order
from billing.models import BillingProfile
# Create your views here.


def cart_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'cart/home.html', {'cart':cart_obj}) 

def cart_update(request):
    post_id = request.POST.get('post_id')
    post_obj = get_object_or_404(Post, id=post_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    if post_obj in cart_obj.post.all():
        cart_obj.post.remove(post_obj)
        cart_icon_1 = 'text-success'
        cart_icon_2 = 'text-danger'
    else:
        cart_obj.post.add(post_obj)
        cart_icon_1 = 'text-danger'
        cart_icon_2 = 'text-success'


    cart_count = cart_obj.post.count()

    return JsonResponse({
        "cart_icon_1": cart_icon_1,
        'cart_icon_2': cart_icon_2,
        'cart_count': cart_count,
        'cart_total': cart_obj.total,
        'cart_subtotal': cart_obj.subtotal,
            })

def checkout(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.post.count() == 0:
        return redirect('cart:cart')
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    
    user = request.user
    billing_profile = None
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        }
    return render(request, 'cart/checkout.html', context)