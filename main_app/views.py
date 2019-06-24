from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from shopify_auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.core.mail import EmailMessage
from django.db.models import Q
from django.utils.crypto import get_random_string
from models import AuthAppShopUser, AuthShop, Customer, Weather, Order, Countnumber
from GoodWeather import settings
from shopify_webhook.decorators import webhook
import shopify


@csrf_exempt
@webhook
def uninstall_webhook_callback(request):
  print '++++++++++++++++++ deleting webhook ++++++++++++++++++'
  webhook_data = request.webhook_data
  print webhook_data['domain']
  print request.webhook_domain
  try:
    user = AuthAppShopUser.objects.filter(myshopify_domain=request.webhook_domain).order_by('-id')[0]
    user.delete()
  except:
    pass
  try:
    current_shop = AuthShop.objects.filter(shop_name=request.webhook_domain).order_by('-id')[0]
    current_shop.delete()
  except:
    pass
  print('webhook ok')
  return HttpResponse('ok')

@login_required
def home(request, *args, **kwargs):
  print '++++++++++++++++++ activating webhook ++++++++++++++++++'
  webhook_shop_address = 'https://9731e621.ngrok.io' + '/app/uninstall_webhook_callback/'
  with request.user.session:
    webhook_status = 0
    webhook_shops = shopify.Webhook.find()
    if webhook_shops:
      for webhook_shop in webhook_shops:
        if webhook_shop.address == webhook_shop_address:
          webhook_status = 1
    if webhook_status == 0:
      print '++++++++++++++++++ saving webhook ++++++++++++++++++'
      webhook_shop = shopify.Webhook()
      webhook_shop.topic = 'app/uninstalled'
      webhook_shop.address = webhook_shop_address
      webhook_shop.format = 'json'
      webhook_shop.save()
  print '++++++++++++++++++++++++++ shopify store information ++++++++++++++++++++'
  shop_name = request.user.myshopify_domain
  print shop_name
  shop_id = ''
  with request.user.session:
    shop = shopify.Shop.current()
    shop_id = str(shop.id)
  print shop_id
  try:
    current_shop = AuthShop.objects.filter(shop_name=shop_name)[0]
    current_shop.shop_id = shop_id
    current_shop.save()
  except:
    print '++++++++++++++++++ current shop id error ++++++++++++++++++'
    pass
  try:
    current_info = Countnumber.objects.filter(shop_name=shop_name).order_by('-id')[0]
    sun_today_number = current_info.sun_today
    rain_today_number = current_info.rain_today
    wind_today_number = current_info.wind_today
    snow_today_number = current_info.snow_today
    sun_tomorrow_number = current_info.sun_tomorrow
    rain_tomorrow_number = current_info.rain_tomorrow
    wind_tomorrow_number = current_info.wind_tomorrow
    snow_tomorrow_number = current_info.snow_tomorrow
    sun_week_number = current_info.sun_week
    rain_week_number = current_info.rain_week
    wind_week_number = current_info.wind_week
    snow_week_number = current_info.snow_week
  except:
    sun_today_number = '0'
    rain_today_number = '0'
    wind_today_number = '0'
    snow_today_number = '0'
    sun_tomorrow_number = '0'
    rain_tomorrow_number = '0'
    wind_tomorrow_number = '0'
    snow_tomorrow_number = '0'
    sun_week_number = '0'
    rain_week_number = '0'
    wind_week_number = '0'
    snow_week_number = '0'

  csv_name = shop_id + '.csv'

  return render(request, "main_app/installation.html", 
    {
      'csv_name': csv_name,
      'sun_today_number': sun_today_number,
      'rain_today_number': rain_today_number,
      'wind_today_number': wind_today_number,
      'snow_today_number': snow_today_number,
      'sun_tomorrow_number': sun_tomorrow_number,
      'rain_tomorrow_number': rain_tomorrow_number,
      'wind_tomorrow_number': wind_tomorrow_number,
      'snow_tomorrow_number': snow_tomorrow_number,
      'sun_week_number': sun_week_number,
      'rain_week_number': rain_week_number,
      'wind_week_number': wind_week_number,
      'snow_week_number': snow_week_number,
    })

@login_required
def show_list(request, day, weather, *args, **kwargs):
  #  getting the shop id from session
  print '++++++++++++++++++++++ shopify store inforamtion ++++++++++++++++++'
  shop_name = request.user.myshopify_domain
  print shop_name
  shop_id = ''
  with request.user.session:
    shop = shopify.Shop.current()
    shop_id = str(shop.id)
  print shop_id
  search_key = ''
  if request.method == 'POST':
    search_key = request.POST.get('search_key')
    day = request.POST.get('day')

  count_number = 0
  result = []
  query = Q()
  if day == 'today':
    if search_key == '':
      query = Q(shop_name=shop_name)&Q(today__contains=weather)
    else:
      query = (Q(shop_name=shop_name)&Q(today__contains=weather))|Q(city__contains=search_key)|Q(province__contains=search_key)|Q(country__contains=search_key)
  if day == 'tomorrow':
    if search_key == '':
      query = Q(shop_name=shop_name)&Q(tomorrow__contains=weather)
    else:
      query = (Q(shop_name=shop_name)&Q(tomorrow__contains=weather))|Q(city__contains=search_key)|Q(province__contains=search_key)|Q(country__contains=search_key)
  if day == 'week':
    if search_key == '':
      query = Q(shop_name=shop_name)&Q(week__contains=weather)
    else:
      query = (Q(shop_name=shop_name)&Q(week__contains=weather))|Q(city__contains=search_key)|Q(province__contains=search_key)|Q(country__contains=search_key)
  result = Customer.objects.filter(query)
  count_number = result.count()
  # return the values to template.
  return render(request, "main_app/customer_list.html", 
    {
      'day': day,
      'weather': weather,
      'count_number': count_number,
      'customers': result,
      'csv_name': shop_id + '-' + day + '-' + weather + '.csv',
      'search_key': search_key
    })
