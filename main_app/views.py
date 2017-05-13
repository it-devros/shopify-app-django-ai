from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from shopify_auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMessage
from django.db.models import Q
from django.utils.crypto import get_random_string
from models import AuthAppShopUser
from GoodWeather import settings
from shopify_webhook.decorators import webhook


@login_required
def home(request, *args, **kwargs):
    return render(request, "main_app/installation.html",
        {   
     })
