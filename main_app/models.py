from shopify_auth.models import AbstractShopUser
from django.db import models

# the shop user model for authentication and management of store.

class AuthAppShopUser(AbstractShopUser):
	pass


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

	saved_at = models.DateField(auto_now_add=True)

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
	oid = models.CharField(max_length=20, null=True)
	name = models.CharField(max_length=20, null=True)
	number = models.CharField(max_length=20, null=True)
	items = models.CharField(max_length=20, null=True)
	city = models.CharField(max_length=255, null=True)
	province = models.CharField(max_length=255, null=True)
	country = models.CharField(max_length=255, null=True)

	def __unicode__(self):
		return "%s" % self.name