from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Item, Coupon

@login_required
def index(request):
    cart = Cart.objects.get(user=request.user, is_bought=False)
    cartitems = CartItem.objects.filter(cart=cart)
    total = 0
    for item in cartitems:
        total += item.price
    return render(request, 'cart/index.html', {
        'cart': cart,
        'cartitems': cartitems,
        'total': total,
    })

@login_required
def add_item(request, pk):
    quantity = request.GET.get('quantity', 0)
    cart = Cart.objects.get(user=request.user, is_bought=False)
    item = get_object_or_404(Item, pk=pk)
    if CartItem.objects.filter(item=item, cart=cart).exists():
        existing_item = CartItem.objects.get(item=item, cart=cart)
        existing_item.quantity = existing_item.quantity + int(quantity)
        existing_item.price = float(existing_item.quantity) * item.price
        existing_item.save()
    else:
        final_price = float(quantity) * item.price
        cartitems = CartItem(item=item, quantity=quantity, price=final_price, cart=cart)
        cartitems.save()
    return redirect('cart:index')

@login_required
def remove_item(request, pk):
    cartitems = CartItem(pk=pk)
    cartitems.delete()
    return redirect('cart:index')

@login_required
def buy(request):
    cart = Cart.objects.get(user=request.user, is_bought=False)
    cart.is_bought = True
    cart.save()
    new_cart = Cart(user=request.user)
    new_cart.save()
    return redirect('dashboard:index')

@login_required
def coupon(request):
    coupon = request.GET.get('coupon', '')
    cart = Cart.objects.get(user=request.user, is_bought=False)
    cartitems = CartItem.objects.filter(cart=cart)
    total = 0
    new_total = 0
    for item in cartitems:
        total += item.price
    
    try:
        coupons = Coupon.objects.get(name=coupon)
        cart.coupon = coupons.percent
        cart.save()
        discount = coupons.percent
        coupon_exists = True
        discount_total = total * float(discount) / 100.0
        new_total = total - discount_total
    except :
        cart.coupon = 0
        cart.save()
        discount = 0
        coupon_exists = False

    return render(request, 'cart/index.html', {
        'cart': cart,
        'cartitems': cartitems,
        'total': total,
        'new_total': new_total,
        'discount': discount,
        'coupon_exists': coupon_exists,
    })
