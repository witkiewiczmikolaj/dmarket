from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Item

@login_required
def index(request):
    cart = Cart.objects.get(user=request.user)
    cartitems = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/index.html', {
        'cart': cart,
        'cartitems': cartitems,
    })

@login_required
def add_item(request, pk):
    cart = Cart.objects.get(user=request.user)
    item = get_object_or_404(Item, pk=pk)
    cartitems = CartItem(item=item, price=item.price, cart=cart)
    cartitems.save()
    return redirect('cart:index')

@login_required
def remove_item(request, pk):
    cartitems = CartItem(pk=pk)
    cartitems.delete()
    return redirect('cart:index')
