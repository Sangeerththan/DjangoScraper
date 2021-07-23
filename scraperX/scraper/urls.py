from django.urls import path
from .views import home_page, login_page
from . import views

urlpatterns = [
    path('', home_page, name='home_page'),
     path('/login', login_page, name='login'),
]