from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import (AuthenticationForm,
                                       PasswordChangeForm)
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages

from PIL import Image

from . import forms


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('accounts:profile'))
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = forms.CreateUserForm()
    if request.method == 'POST':
        form = forms.CreateUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/sign_up.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@never_cache
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = forms.UpdateUserForm(request.POST,
                                    request.FILES or None,
                                    instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile is updated!'
            )
            return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        form = forms.UpdateUserForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Password updated! Please login with your new password')
            return HttpResponseRedirect(reverse('accounts:sign_in'))
    else:
        form = PasswordChangeForm(user=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/change_password.html', context)


@login_required
def edit_avatar(request):
    avatar = request.user.avatar
    if request.method == 'POST':
        form = forms.AvatarEditForm(request.POST,
                                    request.FILES or None)
        if form.is_valid():
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            width = form.cleaned_data.get('width')
            height = form.cleaned_data.get('height')
            rotate = form.cleaned_data.get('rotate')
            image = Image.open(avatar)
            image = image.crop((x, y, width + x, height + y))
            image = image.rotate(-rotate, expand=True)
            if form.cleaned_data.get('scaleX') == -1:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            image.save(avatar.path)
            return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        form = forms.AvatarEditForm()

    context = {
        'form': form,
        'avatar': avatar
    }
    return render(request, 'accounts/edit_avatar.html', context)
