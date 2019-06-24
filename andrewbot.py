import csv
import yweather
import urllib2, urllib, json, pdb
import sqlite3
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

print '+++++++++++++ connecting database ++++++++++++++++++++'
sqlite_file = './db.sqlite3'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

print '+++++++++++++ getting all shops ++++++++++++++++++++'
c.execute('SELECT * FROM main_app_authshop')
all_rows = c.fetchall()

print '+++++++++++++ main action ++++++++++++++++++++'

for row in all_rows:
  print '+++++++++++++ shop information ++++++++++++++++++++'
  print row[1], row[2], row[3]
  shop_name = row[1]
  url = 'https://' + row[1]
  shop_id = row[2]
  access_token = row[3]

  print '+++++++++++++ deleting 250 orders data for each shop ++++++++++++++++++++'
  t = (shop_name,)
  c.execute('DELETE FROM main_app_order WHERE shop_name=?', t)
  conn.commit()
  print '+++++++++++++ getting 250 orders data for each shop ++++++++++++++++++++'
  i = 1
  result_no = []
  while i < 6:
    request_url = url + '/admin/orders.json?limit=50&page=' + str(i)
    req = urllib2.Request(request_url)
    req.add_header('X-Shopify-Access-Token', access_token)
    try:
      result = urllib2.urlopen(req).read().encode('raw-unicode-escape')
      orders = json.loads(result)
      for order in orders['orders']:
        items = ''
        for item in order['line_items']:
          items += item['name'] + ', '
        items = items[:-2]
        print '++++++++++++++++ without shipping address ++++++++++++'
        print order['id'], order['name'], order['order_number'], items
        result_no.append((shop_name, order['id'], order['name'], order['order_number'], items))
    except:
      print '++++++++++++++ orders error ++++++++++++++++++++'
    i += 1

  print '+++++++++++++++++ saving orders ++++++++++++++++++'
  if result_no:
    c.executemany('INSERT INTO main_app_order(shop_name, order_id, name, order_number, items) VALUES (?,?,?,?,?)', result_no)
  conn.commit()

  print '+++++++++++++++++++ getting customers ++++++++++++++++++++++++++'
  request_url = url + '/admin/customers/count.json'
  print request_url
  req = urllib2.Request(request_url)
  req.add_header('X-Shopify-Access-Token', access_token)
  count = urllib2.urlopen(req).read()
  data = json.loads(count)
  pagi_num = int(data['count'])/50
  if int(data['count'])%50 != 0:
    pagi_num += 1
  print '+++++++++++++++++++++++++++ pagi num ++++++++++++++++++'
  print pagi_num
  i = 1
  result_ok = []
  result_no = []
  while i < pagi_num:
    request_url = url + '/admin/customers.json?limit=50&page=' + str(i)
    req = urllib2.Request(request_url)
    req.add_header('X-Shopify-Access-Token', access_token)
    try:
      result = urllib2.urlopen(req).read().encode('raw-unicode-escape')
      customers = json.loads(result)
      for customer in customers['customers']:
        print '+++++++++++++++++++++++++ customer data loading ++++++++++++++++++'
        t = (shop_name, customer['email'],)
        c.execute('SELECT * FROM main_app_customer WHERE shop_name=? and email=?', t)
        current_customer = c.fetchall()
        addr = []
        try:
          addr = customer['default_address']
        except:
          print '++++++++++++++++ default address error detected +++++++++++'
          addr = []
        if not current_customer and addr:
          print '++++++++++++++++++++++++ new customer +++++++++++++++++++'
          result_ok.append((shop_name, addr['address1'], addr['address2'], addr['city'], addr['country'], addr['first_name'], addr['id'], addr['last_name'], addr['phone'], addr['province'], addr['zip'], addr['province_code'], addr['country_code'], customer['email'], customer['total_spent'], customer['created_at'], customer['updated_at'],))
        else:
          print '++++++++++++++++++++++++ updating customer +++++++++++++++++++'
          if addr:
            result_no.append((addr['address1'], addr['address2'], addr['city'], addr['country'], addr['first_name'], addr['id'], addr['last_name'], addr['phone'], addr['province'], addr['zip'], addr['province_code'], addr['country_code'], customer['total_spent'], customer['updated_at'], shop_name, customer['email'],))

    except:
      print '+++++++++++++++++++ getting the customers error +++++++++++++++'
    i += 1

  print '+++++++++++++++++ saving customers ++++++++++++++++++'
  if result_ok:
    print '++++++++++++++++++ new ++++++++++++++++++'
    c.executemany('INSERT INTO main_app_customer(shop_name, address1, address2, city, country, first_name, addr_id, last_name, phone, province, zip_code, province_code, country_code, email, total_spent, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', result_ok)
  if result_no:
    print '+++++++++++++++++++ update +++++++++++++++++'
    c.executemany('UPDATE main_app_customer SET address1=?, address2=?, city=?, country=?, first_name=?, addr_id=?, last_name=?, phone=?, province=?, zip_code=?, province_code=?, country_code=?, total_spent=?, updated_at=? WHERE shop_name=? and email=?', result_no)
  conn.commit()


  print '++++++++++++++++++++ getting customers ++++++++++++++++++'

  t = (shop_name,)
  c.execute('SELECT * FROM main_app_customer WHERE shop_name=?', t)
  customers = c.fetchall()

  print '++++++++++++++++++++ calculating information ++++++++++++++++++++'

  if customers:
    print '+++++++++++++++++ generating csv file +++++++++++++++++'
    csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '.csv'
    with open(csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in customers:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'

    print '+++++++++++++++++++ getting weathers ++++++++++++++++++++++++++'
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    weather_ok = []
    weather_no = []
    city_list = []
    client = yweather.Client()
    for customer in customers:
      if customer[4] and customer[5] and customer[10]:
        city = customer[4]
        city_s = ''
        if customer[13] == 'US':
          city_s = customer[10]
        else:
          city_s = customer[5]
        param = ''
        param = city + ', ' + city_s
        if param != '' and not param in city_list:
          city_list.append(param)
          print param
          try:
            client_woeid = client.fetch_woeid(param)
            print client_woeid
            yql_query = "select * from weather.forecast where woeid=" + client_woeid 
            yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json" 
            result = urllib2.urlopen(yql_url).read()
            data = json.loads(result) 
            data = data['query']['results']
            t = (city, city_s,)
            c.execute('SELECT * FROM main_app_weather WHERE city=? and city_sec=?', t)
            weathers = c.fetchall()
            today = data['channel']['item']['condition']['text']
            tomorrow = data['channel']['item']['forecast'][1]['text']
            temp = ''
            for con in data['channel']['item']['forecast']:
              temp += con['text'] + ', '
            week = temp[:-2]
            if weathers:
              t = (today, tomorrow, week, city, city_s,)
              weather_ok.append(t)
            else:
              t = (city, city_s, today, tomorrow, week,)
              weather_no.append(t)
          except:
            pass

    print '++++++++++++++ saving the weather data ++++++++++++++++++'
    if weather_ok:
      print '++++++++++++++ updating weather data ++++++++++++++++++'
      c.executemany('UPDATE main_app_weather SET today_condition=?, tomorrow_condition=?, week_condition=? WHERE city=? and city_sec=?', weather_ok)
    if weather_no:
      print '++++++++++++++ saving new weather data ++++++++++++++++++'
      c.executemany('INSERT INTO main_app_weather(city, city_sec, today_condition, tomorrow_condition, week_condition) VALUES (?,?,?,?,?)', weather_no)
    conn.commit()

    print '+++++++++++++++++++++++++ values for calculating ++++++++++++++++++++'
    sun_today = 0
    rain_today = 0
    wind_today = 0
    snow_today = 0
    sun_tomorrow = 0
    rain_tomorrow = 0
    wind_tomorrow = 0
    snow_tomorrow = 0
    sun_week = 0
    rain_week = 0
    wind_week = 0
    snow_week = 0
    results = []
    sun_today_list = []
    rain_today_list = []
    wind_today_list = []
    snow_today_list = []
    sun_tomorrow_list = []
    rain_tomorrow_list = []
    wind_tomorrow_list = []
    snow_tomorrow_list = []
    sun_week_list = []
    rain_week_list = []
    wind_week_list = []
    snow_week_list = []
    for customer in customers:
      if customer[4] and customer[5] and customer[10]:
        city = customer[4]
        city_s = ''
        if customer[13] == 'US':
          city_s = customer[10]
        else:
          city_s = customer[5]
        t = (city, city_s,)
        print city, city_s
        c.execute('SELECT * FROM main_app_weather WHERE city=? and city_sec=?', t)
        weathers = c.fetchall()
        if weathers:
          weather = weathers[0]
          today = weather[3]
          if today.find('Sunny') != -1:
            sun_today += 1
            sun_today_list.append(customer)
          if today.find('Rain') != -1:
            rain_today += 1
            rain_today_list.append(customer)
          if today.find('Windy') != -1:
            wind_today += 1
            wind_today_list.append(customer)
          if today.find('Snow') != -1:
            snow_today += 1
            snow_today_list.append(customer)
          tomorrow = weather[4]
          if tomorrow.find('Sunny') != -1:
            sun_tomorrow += 1
            sun_tomorrow_list.append(customer)
          if tomorrow.find('Rain') != -1:
            rain_tomorrow += 1
            rain_tomorrow_list.append(customer)
          if tomorrow.find('Windy') != -1:
            wind_tomorrow += 1
            wind_tomorrow_list.append(customer)
          if tomorrow.find('Snow') != -1:
            snow_tomorrow += 1
            snow_tomorrow_list.append(customer)
          week = weather[5]
          week_list = week.split(',')
          for we in week_list:
            we = we.strip()
            if we.find('Sunny') != -1:
              sun_week += 1
              sun_week_list.append(customer)
            if we.find('Rain') != -1:
              rain_week += 1
              rain_week_list.append(customer)
            if we.find('Windy') != -1:
              wind_week += 1
              wind_week_list.append(customer)
            if we.find('Snow') != -1:
              snow_week += 1
              snow_week_list.append(customer)
          t = (today, tomorrow, week, shop_name, city, city_s, city_s)
          results.append(t)

    print '+++++++++++++++++++ saving the customers week condition ++++++++++++++'
    c.executemany('UPDATE main_app_customer SET today=?, tomorrow=?, week=? WHERE shop_name=? and city=? and (country=? or province=?)', results)
    conn.commit()

    print '+++++++++++++++++++++ saving count numbers +++++++++++++++'
    t = (shop_name,)
    c.execute('SELECT * FROM main_app_countnumber WHERE shop_name=?', t)
    countnumbers = c.fetchall()
    if countnumbers:
      print '++++++++++++++ updating count number ++++++++++++++++++'
      t = (sun_today, rain_today, wind_today, snow_today, sun_tomorrow, rain_tomorrow, wind_tomorrow, snow_tomorrow, sun_week, rain_week, wind_week, snow_week, shop_name,)
      c.execute('UPDATE main_app_countnumber SET sun_today=?, rain_today=?, wind_today=?, snow_today=?, sun_tomorrow=?, rain_tomorrow=?, wind_tomorrow=?, snow_tomorrow=?, sun_week=?, rain_week=?, wind_week=?, snow_week=? WHERE shop_name=?', t)
    else:
      print '++++++++++++++ saving new count number ++++++++++++++++++'
      t = (shop_name, sun_today, rain_today, wind_today, snow_today, sun_tomorrow, rain_tomorrow, wind_tomorrow, snow_tomorrow, sun_week, rain_week, wind_week, snow_week,)
      c.execute('INSERT INTO main_app_countnumber(shop_name, sun_today, rain_today, wind_today, snow_today, sun_tomorrow, rain_tomorrow, wind_tomorrow, snow_tomorrow, sun_week, rain_week, wind_week, snow_week) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', t)
    conn.commit()

    print '++++++++++++++ generating csv files ++++++++++++++++++'
    sun_today_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'today' + '-' + 'sun' + '.csv'
    with open(sun_today_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in sun_today_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'
    rain_today_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'today' + '-' + 'rain' + '.csv'
    with open(rain_today_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in rain_today_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'
    wind_today_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'today' + '-' + 'wind' + '.csv'
    with open(wind_today_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in wind_today_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'
    snow_today_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'today' + '-' + 'snow' + '.csv'
    with open(snow_today_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in snow_today_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'
    sun_tomorrow_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'tomorrow' + '-' + 'sun' + '.csv'
    with open(sun_tomorrow_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in sun_tomorrow_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'
    rain_tomorrow_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'tomorrow' + '-' + 'rain' + '.csv'
    with open(rain_tomorrow_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in rain_tomorrow_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'
    wind_tomorrow_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'tomorrow' + '-' + 'wind' + '.csv'
    with open(wind_tomorrow_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in wind_tomorrow_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'
    snow_tomorrow_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'tomorrow' + '-' + 'snow' + '.csv'
    with open(snow_tomorrow_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in snow_tomorrow_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'
    sun_week_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'week' + '-' + 'sun' + '.csv'
    with open(sun_week_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in sun_week_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'
    rain_week_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'week' + '-' + 'rain' + '.csv'
    with open(rain_week_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in rain_week_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'
    wind_week_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'week' + '-' + 'wind' + '.csv'
    with open(wind_week_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in wind_week_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'
    snow_week_csv_url = './main_app' + '/static/' + 'csv/' + shop_id + '-' + 'week' + '-' + 'snow' + '.csv'
    with open(snow_week_csv_url, 'wb') as f:
      writer = csv.writer(f)
      writer.writerow(['id', 'shop_name', 'address1', 'address2', 'city', 'country', 'first_name', 'addr_id', 'last_name', 'phone', 'province', 'zip_code', 'province_code', 'country_code', 'email', 'total_spent', 'created_at', 'updated_at', 'saved_at'])
      for customer in snow_week_list:
        try:
          writer.writerow(customer)
        except:
          print '++++++++++++++++ all csv error detected +++++++++++'


conn.close()


