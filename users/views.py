from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_protect
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from .models import CustomUser
from cart.views import CartMixin


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        old_session = request.session.session_key
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            cart_mixin = CartMixin()
            cart_mixin.merge_carts(request, old_session)
            return redirect('main:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            old_session = request.session.session_key
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            cart_mixin = CartMixin()
            cart_mixin.merge_carts(request, old_session)            
            return redirect('main:index')
    else:
        form = CustomUserLoginForm
    return render(request, 'users/login.html', {'form': form})


@login_required(login_url='/users/login')
def profile_view(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'users/profile.html', {'user': user})


@login_required(login_url='/users/login')
def edit_account_details(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'users/edit_account_details.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('main:index')
    return render(request, 'users/logout_confirm.html')
