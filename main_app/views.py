from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from shopify_auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMessage
from django.db.models import Q
from django.utils.crypto import get_random_string
from models import AuthAppShopUser, Customer, Weather, Order
from GoodWeather import settings
from shopify_webhook.decorators import webhook
import shopify
import json
import csv
import yweather


@login_required
def home(request, *args, **kwargs):
	# getting the shop name and deleting the old customers' data
	shop_id = ''
	with request.user.session:
		shop = shopify.Shop.current()
		shop_id = str(shop.id)
	Customer.objects.filter(shop_name=shop_id).delete()
	Orders.objects.filter(shop_name=shop_id).delete()
	#  getting the customers'data from shopify API and saving in database.
	with request.user.session:
		customers = shopify.Customer.find()
		for customer in customers:
			for addr in customer.addresses:
				record = Customer(shop_name=shop_id, address1=addr.address1, address2=addr.address2, city=addr.city, country=addr.country, first_name=addr.first_name, addr_id=addr.id, last_name=addr.last_name, phone=addr.phone, province=addr.province, zip_code=addr.zip, province_code=addr.province_code, country_code=addr.country_code, email=customer.email, total_spent=customer.total_spent, created_at=customer.created_at, updated_at=customer.updated_at)
				record.save()

		orders = shopify.Order.find()
		length = len(orders)
		if length < 250:
			i = 0
		else:
			i = length - 250
		while i < length:
			items = ''
			for item in orders[i].line_items:
				items += item.name + ', '
			if not orders[i].shipping_address:
				for addr in orders[i].shipping_address:
					record = Order(shop_name=shop_id, oid=orders[i].id, name=orders[i].name, number=orders[i].order_number, city=addr.city, province=addr.province, country=addr.country, items=items[:-2])
					record.save()
			else:
				record = Order(shop_name=shop_id, oid=orders[i].id, name=orders[i].name, number=orders[i].order_number, items=items[:-2])
				record.save()
			i += 1

	# getting the customers for each shop and making csv and exporting
	customers = Customer.objects.filter(shop_name=shop_id)
	csv_url = settings.PROJECT_PATH + '/main_app' + settings.STATIC_URL + 'csv/' + shop_id + '.csv'
	city_list = []
	with open(csv_url, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
		for customer in customers:
			writer.writerow(get_list(customer))
			if customer.country_code == 'US':
				if not [customer.city, customer.province] in city_list:
					city_list.append([customer.city, customer.province])
			else:
				if not [customer.city, customer.country] in city_list:
					city_list.append([customer.city, customer.country])
	csv_name = shop_id + '.csv'
	
	# getting the weather information and saving in database with updating old data.

	# getting the number of customers for each duration(today, tomorrow, week)
	today_number = 0
	tomorrow_number = 0
	week_number = 0
	for customer in customers:
		city = customer.city
		city_s = ''
		if customer.country_code == 'US':
			city_s = customer.province
		else:
			city_s = customer.country
		try:
			weather_list = Weather.objects.filter(Q(city=city)&Q(city_sec=city_s))
			weather = weather_list[0]
			if weather.today_condition == 'sun':
				today_number += 1
			if weather.tomorrow_condition == 'sun':
				tomorrow_number += 1
			week_list = weather.week_condition.split(',')
			i = 0
			for we in week_list:
				we = we.strip()
				if we.find('sun') != -1:
					i += 1
			week_number += i
		except:
			print '++++++++++++++++++ an error occupied'

	return render(request, "main_app/installation.html", 
		{
			'csv_name': csv_name,
			'today_number': today_number,
			'tomorrow_number': tomorrow_number,
			'week_number': week_number
		})

@login_required
def show_list(request, day, *args, **kwargs):
	shop_id = ''
	with request.user.session:
		shop = shopify.Shop.current()
		shop_id = str(shop.id)

	search_key = ''
	if request.method == 'POST':
		search_key = request.POST.get('search_key')
		day = request.POST.get('day')

	count_number = 0
	result = []
	week_result = []
	week_flag = 0
	if day == 'week':
		week_flag = 1

	csv_url = settings.PROJECT_PATH + '/main_app' + settings.STATIC_URL + 'csv/' + shop_id + '-' + day + '.csv'

	customers = Customer.objects.filter(shop_name=shop_id)
	with open(csv_url, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
		for customer in customers:
			city = customer.city
			city_s = ''
			if customer.country_code == 'US':
				city_s = customer.province
			else:
				city_s = customer.country
			try:
				weather_list = Weather.objects.filter(Q(city=city)&Q(city_sec=city_s))
				weather = weather_list[0]
				if day == 'today':
					if weather.today_condition == 'sun':
						if search_key != '':
							count_number += 1
							if customer.city.find(search_key) != -1 or customer.province.find(search_key) != -1 or customer.country.find(search_key) != -1 or customer.email.find(search_key) != -1:
								result.append(customer)
						else:
							count_number += 1
							result.append(customer)
						writer.writerow(get_list(customer))
				if day == 'tomorrow':
					if weather.tomorrow_condition == 'sun':
						if search_key != '':
							count_number += 1
							if customer.city.find(search_key) != -1 or customer.province.find(search_key) != -1 or customer.country.find(search_key) != -1 or customer.email.find(search_key) != -1:
								result.append(customer)
						else:
							count_number += 1
							result.append(customer)
						writer.writerow(get_list(customer))
				if day == 'week':
					if weather.week_condition.find('sun') != -1:
						if search_key != '':
							if customer.city.find(search_key) != -1 or customer.province.find(search_key) != -1 or customer.country.find(search_key) != -1 or customer.email.find(search_key) != -1:
								count_number += 1
								week_list = weather.week_condition.split(',')
								i = 0
								for we in week_list:
									we = we.strip()
									if we.find('sun') != -1:
										i += 1
								print i
								week_result.append([customer, i])
						else:
							count_number += 1
							week_list = weather.week_condition.split(',')
							i = 0
							for we in week_list:
								we = we.strip()
								if we.find('sun') != -1:
									i += 1
							print i
							week_result.append([customer, i])
						writer.writerow(get_list(customer))
			except:
				print '++++++++++++++++++ an error occupied'

	return render(request, "main_app/customer_list.html", 
		{
			'day': day,
			'count_number': count_number,
			'week_flag': week_flag,
			'customers': result,
			'week_customers': week_result,
			'csv_name': shop_id + '-' + day + '.csv',
			'search_key': search_key
		})


def get_list(customer):
	return [customer.shop_name, customer.address1, customer.address2, customer.city, customer.country, customer.first_name, customer.addr_id, customer.last_name, customer.phone, customer.province, customer.zip_code, customer.province_code, customer.country_code, customer.email, customer.total_spent, customer.created_at, customer.updated_at, customer.saved_at]