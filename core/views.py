from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from item.models import Category, Item, User
from cart.models import Cart, Coupon
from core.models import Recomendation
from .forms import SignupForm
from .tokens import account_activation_token

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        Cart(user=user).save()
        Recomendation(user=user).save()
        messages.success(request, "You can now log in!")
        return redirect('/login/')
    else:
        messages.error(request, "Activation link is invalid")

    return redirect('/login/')

def activateemail(request, user, to_email):
    mail_subject = 'Activate your account'
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"{user} check email {to_email} and click the link to activate an account.")
    else:
        messages.success(request, f"Problem sending email to {to_email}, check if email is correct.")

def index(request):
    items = Item.objects.filter(is_sold=False).order_by('-created_at')[0:6]
    categories = Category.objects.all()
    u_r = Recomendation.objects.get(user=request.user)
    u_r_array = [u_r.Beauty, u_r.Clothes, u_r.Electronics, u_r.Furnitures, u_r.Sport, u_r.Toys]
    if u_r_array == [0,0,0,0,0,0]:
        recomendations_exist = False
    else:
        recomendations_exist = True
    u_r_index = u_r_array.index(max(u_r_array))
    recomendations = Item.objects.filter(is_sold=False, category=categories[u_r_index])
    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
        'recomendations': recomendations,
        'recomendations_exist': recomendations_exist,
    })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateemail(request, user, form.cleaned_data.get('email'))
            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })

def logoutuser(request):
    logout(request)
    return redirect('/')
