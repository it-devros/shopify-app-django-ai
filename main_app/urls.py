from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^list/(?P<day>[\w\-]+)/(?P<weather>[\w\-]+)', views.show_list, name='show_list'),
  url(r'^uninstall_webhook_callback/', views.uninstall_webhook_callback, name='uninstall_webhook_callback')
]