from django.shortcuts import render, redirect
from account.forms import RegisterForm, ProfileUpdateForm
from account.models import Profile
from products.models import Cart, Product
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from utils.email import send_email_confirm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            sent_email_confirm(request, user, user.email)
            return redirect('account:login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            session_cart = request.session.get(settings.CART_SESSION_ID)
            if session_cart:
                cart = user.cart
                for product_id, amount in session_cart.items():
                    product = Product.objects.get
                    cart_item, created = CartItem.objects.get(cart=cart, product=product)

                    if not created:
                        cart_item.amount += amount

                    else:
                        cart_item.amount = amount

                    cart_item.save()
                request.session[settings.CART_SESSION_ID] = {}
            next_url = request.GET.get('next')
            return redirect(next_url or 'index')
        else:
            return render(request, 'login.html', {'error': 'incorrect login or password'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def profile_view(request):
    profile = request.user.cart
    return render(request, 'profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            new_email = form.cleaned_data.get('email')
            if new_email != user.email:
                sent_email_confirm(request, user, new_email)
            avatar = form.cleaned_data.get('avatar')
            if avatar:
                profile.avatar = avatar

            profile.save()
            return redirect('account:profile')

    else:
        form = ProfileUpdateForm(user=user)

    return render(request, 'edit_profile.html', {'form': form, 'profile': profile,})
