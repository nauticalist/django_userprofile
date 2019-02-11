from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordChangeForm)
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from . import forms

# Create your views here.

def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return redirect('/accounts/profile')  # TODO: go to profile
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
            return redirect('/accounts/profile')  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})

@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = forms.UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile is updated!'
            )
            return redirect('/accounts/profile')
    else:
        form = forms.UpdateUserForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/edit_profile.html', context)
