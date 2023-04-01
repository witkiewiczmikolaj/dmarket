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
        return render(request, 'dashboard/index.html', {
        'items': items
    })

def cart(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    cartitems = CartItem.objects.filter(cart=cart)
    total = 0
    for item in cartitems:
        total += item.price
    return render(request, 'dashboard/cart.html', {
        'cart': cart,
        'cartitems': cartitems,
        'total': total,
    })