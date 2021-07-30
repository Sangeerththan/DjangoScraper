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
from bs4 import BeautifulSoup # for scraping webpages
import time  
from bs4.element import Tag
import numpy as np
import matplotlib.pyplot as plt


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
        url = 'https://www.landsofamerica.com/United-States/all-land/'
    context = scrape(url)
    title = context['Title']
    urls = context['URL']
    description = context['Description']
    scrape_output = {'title': title, 'urls': urls, 'description': description}
    data = {'scrape_output': scrape_output}
    return render(request, "accounts/manage-data.html", context=data)

def scrape(url):
    data = {}
    r = requests.get(url, data=data)
    html = r.text
    output_dict = scrapeFromHtml(html)
    df = pd.DataFrame(output_dict, columns = output_dict.keys())
    df = df.iloc[:25]
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    t= ax.table(cellText=df.values, colWidths=[0.4, 0.5, 0.3], colLabels=df.columns,  loc='center')
    t.auto_set_font_size(False) 
    t.set_fontsize(6)
    plt.savefig('./static_dir/imgs/scrapetable.png')
    df.to_csv("data.csv", index=False)
    return output_dict

def scrapeFromHtml(html):
    soup = BeautifulSoup(html,'html.parser')
    result_div = soup.find_all('div')

    links = []
    titles = []
    descriptions = []
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href=True)
            title = None
            title = r.find('h3')

            # if isinstance(title,Tag):
            #     title = title.get_text()

            # description = None
            # description = r.find('span', attrs={'class': 'page_article'})

            # if isinstance(description, Tag):
            #     description = description.get_text()

            # Check to make sure everything is present before appending
            if link != '':
                if len(link['href']) > 50:
                    link['href'] = link['href'][0:50]
                links.append(link['href'])
                titles.append(title)
                # descriptions.append(description)
        # Next loop if one element is not present
        except Exception as e:
            print(e)
            continue
    output_dict = {'Title':titles, 'URL': links, 'Description':descriptions}
    return output_dict
