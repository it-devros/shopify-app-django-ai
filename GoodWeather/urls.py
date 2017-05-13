from django.conf.urls import include, url

from main_app.views import home
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'login/', include('shopify_auth.urls')),
    url(r'app/', include('main_app.urls')),
    url(r'^$', home, name='home')
]
