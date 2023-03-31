from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from item.models import Item, User

@login_required
def index(request):
    items = Item.objects.filter(created_by=request.user)
    wishlist = Item.objects.filter(wishlist=request.user)
    return render(request, 'dashboard/index.html', {
        'items': items,
        'wishlist': wishlist
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