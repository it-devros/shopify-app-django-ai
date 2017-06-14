
Documentation of GoodWeather App (Shopify Embedded App)

Preinstallation

- python 2.7.13
- pip, setuptools
- virtualenv

How to set up

- you have to install the python libraries in the requirements.txt
	pip install Django==1.9
	pip install python-dotenv==0.1.0
	pip install ShopifyAPI
- you have to set the app in your app.myshopify.com account.
	you have to follow steps in creating app.
	here you have to put in the App URL and redirection URL like this:
		App URL : [your domain]
		redirection URL : [your domain]/login/finalize
- here you have to get the app API key and secret key.
- and you have to change the app settings in settings.py with app API key and secret key.
	SHOPIFY_APP_NAME = 'GoodWeather'
	SHOPIFY_APP_API_KEY = '[your app api key]'
	SHOPIFY_APP_API_SECRET = '[your app api secret]'
	SHOPIFY_APP_API_SCOPE = ['read_products', 'read_orders', 'write_script_tags', 'read_customers']
	SHOPIFY_APP_IS_EMBEDDED = True
	SHOPIFY_APP_DEV_MODE = False
- you have to run the project.
	python manage.py runserver





