from django.contrib import admin
from django.urls import include, path
from scraper.views import home_page

urlpatterns = [
    path('scraper/', include('scraper.urls')),
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
]
