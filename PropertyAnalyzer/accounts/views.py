from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import LoginForm, RegisterForm, UpdateProfileForm


import requests
import re, json
import pandas as pd
import ast
from datetime import datetime
from urllib.request import urlopen


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
        return redirect('account:manage-data')
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

def manage_data_page(request):
    return render(request, "accounts/manage-data.html")

def dashboard_page(request):
    return render(request, "accounts/dashboard.html")

def scrape_page(request):
    if request.method == "POST":
        if ('url' in request.POST):
            url = request.POST.get('url', 'https://www.sothebysrealty.com/eng/sales/usa')
    else:
        url = 'https://parade.com/937586/parade/life-quotes/'
        # url = "http://www.ibex.bg/ajax/tenders_ajax.php"
    di = scrape(url)
    print(di)
    return render(request, "accounts/manage-data.html")

def scrape(url):
    data = {}
    r = requests.get(url, data=data)
    matches = r.text
    # sort = (sorted(matches, key=lambda k: datetime.strptime(k, '%d.%m.%Y')))
    print("Available Dates: "+str(type(matches)))
    opa = re.findall(r"\w+ly", matches)
    # convert = [ast.literal_eval(x) for x in opa]
    df = pd.DataFrame(opa)
    print(df)
    df.to_csv("data.csv", index=False)
    res_dct = {}
    # res_dct = {convert[i]: convert[i + 1] for i in range(0, len(convert), 2)}
    return res_dct

# def scrape(url):
#     url = "https://quotes.yourdictionary.com/wikipedia"
#     hdr = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#             'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'         
#     }
#     page = urlopen(url, data=bytes(json.dumps(hdr), encoding="utf-8"))
#     html = page.read().decode("ascii")
#     pattern = "<title.*?>.*?</title.*?>"
#     match_results = re.search(pattern, html, re.IGNORECASE)
#     title = match_results.group()
#     title = re.sub("<.*?>", "", title) # Remove HTML tags
#     convert = [ast.literal_eval(x) for x in ti]
#     return title