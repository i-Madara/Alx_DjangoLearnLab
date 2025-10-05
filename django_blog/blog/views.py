from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def index(request):
    return render(request, 'blog/index.html')

def register(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('profile')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created. Please log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/auth/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')  # PRG pattern
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'blog/auth/profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })
