from django.urls import path

from .views import account_home_page, login_page, logout_page, register_page,dashboard_page, manage_data_page, scrape


app_name = 'account'

urlpatterns = [
    path('home/', account_home_page, name='account-home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('manageData/',manage_data_page, name='manage-data'),
    path('dashboard/',dashboard_page, name='dashboard'),
    path('scrape/',scrape, name='scrape')
]