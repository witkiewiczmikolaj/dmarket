from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from item.models import Item, User
from cart.models import Cart, CartItem

@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user)
    wishlist = Item.objects.filter(wishlist=request.user)
    past_carts = Cart.objects.filter(user=request.user, is_bought=True)
    return render(request, 'dashboard/index.html', {
        'items': items,
        'wishlist': wishlist,
        'past_carts': past_carts
    })

def user(request, pk):
    user = get_object_or_404(User, pk=pk)
    items = Item.objects.filter(created_by=user)
    if user != request.user:
        return render(request, 'dashboard/user.html', {
            'user': user,
            'items': items
        })
    else:
        wishlist = Item.objects.filter(wishlist=request.user)
        past_carts = Cart.objects.filter(user=request.user, is_bought=True)
        return render(request, 'dashboard/index.html', {
        'items': items,
        'wishlist': wishlist,
        'past_carts': past_carts
    })

def cart(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    cartitems = CartItem.objects.filter(cart=cart)
    total = 0
    new_total = 0
    coupon_exists = False
    for item in cartitems:
        total += item.price
    if cart.coupon != 0:
        coupon_exists = True
        discount = cart.coupon
        discount_total = total * float(discount) / 100.0
        new_total = total - discount_total
    return render(request, 'dashboard/cart.html', {
        'cart': cart,
        'cartitems': cartitems,
        'total': total,
        'new_total': new_total,
        'coupon_exists': coupon_exists,
    })