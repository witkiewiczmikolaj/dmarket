from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Item, Category, Review, User
from .forms import NewItemForm, EditItemForm, ReviewForm

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categrories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categrories,
        'category_id': int(category_id),
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    reviews = Review.objects.filter(item=item).order_by('-created_at')
    if reviews:
        rating_sum = 0
        for rating in range(len(reviews.values_list('stars'))):
            rating_sum += reviews.values_list('stars')[rating][0]
        stars = round(rating_sum/len(reviews.values_list('stars')),2)
    else:
        stars = 0

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review_msg = form.save(commit=False)
            review_msg.item = item
            review_msg.created_by = request.user
            review_msg.save()

            return redirect('item:detail', pk=pk)
    else:
        form = ReviewForm()


    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'reviews': reviews,
        'form': form,
        'stars': stars,
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item'
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item'
    })

@login_required
def addwishlist(request, pk):
    item = get_object_or_404(Item, pk=pk)
    user = get_object_or_404(User, pk=request.user.id)
    item.wishlist.add(user)
    return redirect('dashboard:index')

@login_required
def removewishlist(request, pk):
    item = get_object_or_404(Item, pk=pk)
    user = get_object_or_404(User, pk=request.user.id)
    item.wishlist.remove(user)
    return redirect('dashboard:index')