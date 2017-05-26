from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/(?P<day>[\w\-]+)', views.show_list, name='show_list'),
]