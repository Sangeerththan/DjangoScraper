from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import LoginForm, RegisterForm, UpdateProfileForm

# Create your views here.


def account_home_page(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login. You cannot access this page!")
        return redirect("account:login")
    context = {}
    return render(request, "accounts/account-home.html", context=context)

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'title': "Please Login!", 
        'form': form,
    }
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        print("User Logged in : ", request.user.is_authenticated)
        # Redirect to a success page.
        messages.success(request, "Login Successful.")
        return redirect('/')
    else:
        # Return an 'invalid login' error message.
        print("Error...")
    
    return render(request, 'accounts/login.html', context=context)

def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'title': "Register Yourself", 
        'form': form,
    }
    username = request.POST.get('username')
    email    = request.POST.get('email')
    password = request.POST.get('password')
    if form.is_valid():
        user = User.objects.create_user(username=username, email=email, password=password)
        print("User created : ", user)
        messages.success(request, f"User: - '{user}' successfully Added.")
        print(form.cleaned_data)
    return render(request, 'accounts/register.html', context=context)


def logout_page(request):
    if request.user.is_authenticated:
        print("User logged out : ", request.user)
        messages.success(request, "Logged Out ")
        logout(request)
        return redirect("account:login")
    else:
        messages.error(request, "Logging out failed...")




def update_profile(request):
    if request.user.is_authenticated:
        update_form = UpdateProfileForm(request.POST or None, instance=request.user)
        if update_form.is_valid():
            profile_instance = update_form.save(commit=False)
            profile_instance.first_name = request.POST.get('first_name')
            profile_instance.last_name = request.POST.get('last_name')
            profile_instance.save()
            messages.success(request, "You profile details updated successfully.")
            return redirect("account:account-home")
    else:
        messages.warning(request, "Please Login. You cannot access this page!")
        return redirect("account:login")

    context = {
        'update_form': update_form,
    }
    return render(request, "accounts/account-profile.html", context=context)
