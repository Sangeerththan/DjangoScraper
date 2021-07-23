from django.shortcuts import render
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail

from .forms import ContactForm
# Create your views here.

def home_page(request):
    return render(request, 'home_page.html')
