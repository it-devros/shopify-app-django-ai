from shopify_auth.models import AbstractShopUser
from django.db import models

# the shop user model for authentication and management of store.

class AuthAppShopUser(AbstractShopUser):
	pass

class AuthShop(models.Model):
	shop_name = models.CharField(max_length=255, unique=True, editable=False)
	shop_id = models.CharField(max_length=255, unique=True, editable=False)
	token = models.CharField(max_length=32, editable=False, default='00000000000000000000000000000000')
	
	def __unicode__(self):
		return "%s" % self.shop_name


class Customer(models.Model):
	shop_name = models.CharField(max_length=255, null=True)
	address1 = models.CharField(max_length=255, null=True)
	address2 = models.CharField(max_length=255, null=True)
	city = models.CharField(max_length=127, null=True)
	country = models.CharField(max_length=127, null=True)
	first_name = models.CharField(max_length=127, null=True)
	addr_id = models.CharField(max_length=127, null=True)
	last_name = models.CharField(max_length=127, null=True)
	phone = models.CharField(max_length=18, null=True)
	province = models.CharField(max_length=54, null=True)
	zip_code = models.CharField(max_length=10, null=True)
	province_code = models.CharField(max_length=5, null=True)
	country_code = models.CharField(max_length=5, null=True)
	email = models.CharField(max_length=127, null=True)
	total_spent = models.CharField(max_length=127, null=True)
	created_at = models.CharField(max_length=54, null=True)
	updated_at = models.CharField(max_length=54, null=True)
	today = models.CharField(max_length=255, null=True)
	tomorrow = models.CharField(max_length=255, null=True)
	week = models.CharField(max_length=255, null=True)

	def __unicode__(self):
		return "%s" % self.shop_name

class Weather(models.Model):
	city = models.CharField(max_length=255, null=True)
	city_sec = models.CharField(max_length=255, null=True)
	today_condition = models.CharField(max_length=255, null=True)
	tomorrow_condition = models.CharField(max_length=255, null=True)
	week_condition = models.CharField(max_length=255, null=True)

	def __unicode__(self):
		return "%s" % self.city

class Order(models.Model):
	shop_name = models.CharField(max_length=255, null=True)
	order_id = models.CharField(max_length=20, null=True)
	name = models.CharField(max_length=20, null=True)
	order_number = models.CharField(max_length=20, null=True)
	items = models.CharField(max_length=20, null=True)
	city = models.CharField(max_length=255, null=True)
	province = models.CharField(max_length=255, null=True)
	country = models.CharField(max_length=255, null=True)

	def __unicode__(self):
		return "%s" % self.name

class Countnumber(models.Model):
	shop_name = models.CharField(max_length=255, null=True)
	sun_today = models.CharField(max_length=20, null=True)
	rain_today = models.CharField(max_length=20, null=True)
	wind_today = models.CharField(max_length=20, null=True)
	snow_today = models.CharField(max_length=20, null=True)
	sun_tomorrow = models.CharField(max_length=20, null=True)
	rain_tomorrow = models.CharField(max_length=20, null=True)
	wind_tomorrow = models.CharField(max_length=20, null=True)
	snow_tomorrow = models.CharField(max_length=20, null=True)
	sun_week = models.CharField(max_length=20, null=True)
	rain_week = models.CharField(max_length=20, null=True)
	wind_week = models.CharField(max_length=20, null=True)
	snow_week = models.CharField(max_length=20, null=True)

	def __unicode__(self):
		return "%s" % self.shop_name