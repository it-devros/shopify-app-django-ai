import psycopg2
import csv
import yweather
import urllib2, urllib, json, pdb





Order.objects.filter(shop_name=shop_id).delete()

	#  getting the customers'data and orders' data from shopify API and saving in database.
	with request.user.session:
		request_url = 'https://' + request.user.myshopify_domain + '/admin/customers/count.json'
		print request_url
		req = urllib2.Request(request_url)
		req.add_header('X-Shopify-Access-Token', request.user.token)
		count = urllib2.urlopen(req).read()
		data = json.loads(count)
		pagi_num = int(data['count'])/50
		if int(data['count'])%50 != 0:
			pagi_num += 1
		print '+++++++++++++++++++++++++++ pagi num ++++++++++++++++++'
		print pagi_num
		i = 1
		while i <= pagi_num:
			request_url = 'https://' + request.user.myshopify_domain + '/admin/customers.json?limit=50&page=' + str(i)
			req = urllib2.Request(request_url)
			req.add_header('X-Shopify-Access-Token', request.user.token)
			try:
				result = urllib2.urlopen(req).read().encode('raw-unicode-escape')
				customers = json.loads(result)
				for customer in customers['customers']:
					print '+++++++++++++++++++++++++ customer data loading ++++++++++++++++++'
					current_customer = Customer.objects.filter(Q(shop_name=shop_id)&Q(email=customer['email'])).order_by('-id')
					try:
						addr = customer['default_address']
					except:
						print '++++++++++++++++ default address error detected +++++++++++'
						addr = []
					if not current_customer and addr:
						record = Customer(shop_name=shop_id, address1=addr['address1'], address2=addr['address2'], city=addr['city'], country=addr['country'], first_name=addr['first_name'], addr_id=addr['id'], last_name=addr['last_name'], phone=addr['phone'], province=addr['province'], zip_code=addr['zip'], province_code=addr['province_code'], country_code=addr['country_code'], email=customer['email'], total_spent=customer['total_spent'], created_at=customer['created_at'], updated_at=customer['updated_at'])
						print 'new'
						record.save()
					else:
						try:
							current_customer = current_customer[0]
							current_customer.address1 = addr['address1']
							current_customer.address2 = addr['address2']
							current_customer.city = addr['city']
							current_customer.country = addr['country']
							current_customer.first_name = addr['first_name']
							current_customer.addr_id = addr['id']
							current_customer.last_name = addr['last_name']
							current_customer.phone = addr['phone']
							current_customer.province = addr['province']
							current_customer.zip_code = addr['zip']
							current_customer.province_code = addr['province_code']
							current_customer.country_code = addr['country_code']
							current_customer.total_spent = customer['total_spent']
							current_customer.updated_at = customer['updated_at']
							print 'update'
							current_customer.save()
						except:
							print '++++++++++++++++ customer updated error detected +++++++++++'
			except:
				print '++++++++++++++++ unicode error detected +++++++++++'
			i += 1



		request_url = 'https://' + request.user.myshopify_domain + '/admin/orders.json?limit=250'
		print request_url
		req = urllib2.Request(request_url)
		req.add_header('X-Shopify-Access-Token', request.user.token)
		try:
			result = urllib2.urlopen(req).read().encode('raw-unicode-escape')
			orders = json.loads(result)
			for order in orders['orders']:
				items = ''
				for item in order['line_items']:
					items += item['name'] + ', '
				if not order['shipping_address']:
					for addr in order['shipping_address']:
						record = Order(shop_name=shop_id, oid=order['id'], name=order['name'], number=order['order_number'], city=addr['city'], province=addr['province'], country=addr['country'], items=items[:-2])
						record.save()
				else:
					record = Order(shop_name=shop_id, oid=order['id'], name=order['name'], number=order['order_number'], items=items[:-2])
					record.save()
		except:
			print '++++++++++++++ getting order error ++++++++++++++++++'

	# getting the customers for each shop and making csv and exporting
	customers = Customer.objects.filter(shop_name=shop_id)
	csv_url = settings.PROJECT_PATH + '/main_app' + settings.STATIC_URL + 'csv/' + shop_id + '.csv'
	with open(csv_url, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
		for customer in customers:
			try:
				writer.writerow(get_list(customer))
			except:
				print '++++++++++++++++ all csv error detected +++++++++++'
			
	csv_name = shop_id + '.csv'
	
	# getting the weather information and saving in database with updating old data.

	baseurl = "https://query.yahooapis.com/v1/public/yql?"
	client = yweather.Client()
	for customer in customers:
		city = customer.city
		city_s = ''
		if customer.country_code == 'US':
			city_s = customer.province
		else:
			city_s = customer.country
		param = ''
		if city and city_s:
			param = city + ', ' + city_s
		if param != '':
			print param
			try:
				client_woeid = client.fetch_woeid(param)
				print client_woeid
				yql_query = "select * from weather.forecast where woeid=" + client_woeid 
				yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json" 
				result = urllib2.urlopen(yql_url).read()
				data = json.loads(result) 
				data = data['query']['results']
				weathers = Weather.objects.filter(Q(city=city)&Q(city_sec=city_s)).order_by('-id')
				if weathers:
					weather = weathers[0]
					weather.today_condition = data['channel']['item']['condition']['text']
					weather.tomorrow_condition = data['channel']['item']['forecast'][1]['text']
					temp = ''
					for con in data['channel']['item']['forecast']:
						temp += con['text'] + ', '
					weather.week_condition = temp[:-2]
					weather.save()
				else:
					weather = Weather()
					weather.city = city
					weather.city_sec = city_s
					weather.today_condition = data['channel']['item']['condition']['text']
					weather.tomorrow_condition = data['channel']['item']['forecast'][1]['text']
					temp = ''
					for con in data['channel']['item']['forecast']:
						temp += con['text'] + ', '
					weather.week_condition = temp[:-2]
					weather.save()
			except:
				pass

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
			if weather.today_condition == 'Sunny':
				today_number += 1
				print 'today'
			if weather.tomorrow_condition == 'Sunny':
				tomorrow_number += 1
				print 'tomorrow'
			week_list = weather.week_condition.split(',')
			i = 0
			for we in week_list:
				we = we.strip()
				if we.find('Sunny') != -1:
					i += 1
			week_number += i
			print 'week'
		except:
			print '++++++++++++++++++ an error occupied'












# list view

# getting the search key and day type if request method is post
	search_key = ''
	if request.method == 'POST':
		search_key = request.POST.get('search_key')
		day = request.POST.get('day')

	# values you need
	count_number = 0
	result = []
	week_result = []
	week_flag = 0
	if day == 'week':
		week_flag = 1

	# the path of csv for each day type. the pattern is like this, 23903294-today.csv
	csv_url = settings.PROJECT_PATH + '/main_app' + settings.STATIC_URL + 'csv/' + shop_id + '-' + day + '.csv'

	# getting the result with csv file
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
					if weather.today_condition == 'Sunny':
						if search_key != '':
							count_number += 1
							if customer.city.find(search_key) != -1 or customer.province.find(search_key) != -1 or customer.country.find(search_key) != -1 or customer.email.find(search_key) != -1:
								result.append(customer)
						else:
							count_number += 1
							result.append(customer)
						writer.writerow(get_list(customer))
				if day == 'tomorrow':
					if weather.tomorrow_condition == 'Sunny':
						if search_key != '':
							count_number += 1
							if customer.city.find(search_key) != -1 or customer.province.find(search_key) != -1 or customer.country.find(search_key) != -1 or customer.email.find(search_key) != -1:
								result.append(customer)
						else:
							count_number += 1
							result.append(customer)
						writer.writerow(get_list(customer))
				if day == 'week':
					if weather.week_condition.find('Sunny') != -1:
						if search_key != '':
							if customer.city.find(search_key) != -1 or customer.province.find(search_key) != -1 or customer.country.find(search_key) != -1 or customer.email.find(search_key) != -1:
								count_number += 1
								week_list = weather.week_condition.split(',')
								i = 0
								for we in week_list:
									we = we.strip()
									if we.find('Sunny') != -1:
										i += 1
								print i
								week_result.append([customer, i])
						else:
							count_number += 1
							week_list = weather.week_condition.split(',')
							i = 0
							for we in week_list:
								we = we.strip()
								if we.find('Sunny') != -1:
									i += 1
							print i
							week_result.append([customer, i])
						writer.writerow(get_list(customer))
			except:
				print '++++++++++++++++++ an error detected'




def get_list(customer):
	return [customer.shop_name, customer.address1, customer.address2, customer.city, customer.country, customer.first_name, customer.addr_id, customer.last_name, customer.phone, customer.province, customer.zip_code, customer.province_code, customer.country_code, customer.email, customer.total_spent, customer.created_at, customer.updated_at, customer.saved_at]
