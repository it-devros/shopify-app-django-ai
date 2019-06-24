import yweather
client = yweather.Client()
client.fetch_woeid("Oslo, Norway")
'862592'
oslo_weather = client.fetch_weather("862592")

import urllib2, urllib, json 
baseurl = "https://query.yahooapis.com/v1/public/yql?" 
yql_query = "select wind from weather.forecast where woeid=862592" 
yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json" 
result = urllib2.urlopen(yql_url).read() 
data = json.loads(result) 
print data['query']['results']


{
  'channel': {
    'lastBuildDate': 'Thu, 01 Jun 2017 09:15 AM MYT', 
    'atmosphere': {
      'pressure': '999.0', 
      'rising': '0', 
      'visibility': '16.1', 
      'humidity': '90'
    }, 
    'description': 'Yahoo! Weather for Kuala Lumpur, Kuala Lumpur, MY', 
    'language': 'en-us', 
    'title': 'Yahoo! Weather - Kuala Lumpur, Kuala Lumpur, MY', 
    'image': {
      'url': 'http://l.yimg.com/a/i/brand/purplelogo//uh/us/news-wea.gif', 
      'width': '142', 
      'height': '18', 
      'link': 'http://weather.yahoo.com', 
      'title': 'Yahoo! Weather'
    }, 
    'item': {
      'description': '<![CDATA[<img src="http://l.yimg.com/a/i/us/we/52/28.gif"/>\n<BR />\n<b>Current Conditions:</b>\n<BR />Mostly Cloudy\n<BR />\n<BR />\n<b>Forecast:</b>\n<BR /> Thu - Thunderstorms. High: 89Low: 76\n<BR /> Fri - Thunderstorms. High: 88Low: 78\n<BR /> Sat - Partly Cloudy. High: 89Low: 76\n<BR /> Sun - Thunderstorms. High: 88Low: 77\n<BR /> Mon - Thunderstorms. High: 87Low: 76\n<BR />\n<BR />\n<a href="http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-1154781/">Full Forecast at Yahoo! Weather</a>\n<BR />\n<BR />\n(provided by <a href="http://www.weather.com" >The Weather Channel</a>)\n<BR />\n]]>',
       'pubDate': 'Thu, 01 Jun 2017 08:00 AM MYT', 
       'title': 'Conditions for Kuala Lumpur, Kuala Lumpur, MY at 08:00 AM MYT', 
       'long': '101.71727', 
       'forecast': [
         {
           'code': '4', 
           'text': 'Thunderstorms', 
           'high': '89', 
           'low': '76', 
           'date': '01 Jun 2017', 
           'day': 'Th'
         }, 
         {
           'code': '4', 
           'text': 'Thunderstorms', 
           'high': '88', 
           'low': '78', 
           'date': '02 Jun 2017', 
           'day': 'Fri'
         }, 
         {
           'code': '30', 
           'text': 'Partly Cloudy', 
           'high': '89', 
           'low': '76', 
           'date': '03 Jun 2017', 
           'day': 'Sat'
         }, 
         {
           'code': '4', 
           'text': 'Thunderstorms', 
           'high': '88', 
           'low': '77', 
           'date': '04 Jun 2017', 
           'day': 'Sun'
         }, 
         {
           'code': '4', 
           'text': 'Thunderstorms', 
           'high': '87', 
           'low': '76', 
           'date': '05 Jun 2017', 
           'day': 'Mon'
         }, 
         {
           'code': '4', 
           'text': 'Thunderstorms', 
           'high': '88', 
           'low': '76', 
           'date': '06 Jun 2017', 
           'day': 'Tue'
         }, 
         {
           'code': '4', 
           'text': 'Thunderstorms', 
           'high': '87', 
           'low': '76', 
           'date': '07 Jun 2017', 
           'day': 'Wed'
         }, 
         {
           'code': '4', 
           'text': 'Thunderstorms', 
           'high': '88', 
           'low': '76', 
           'date': '08 Jun 2017', 
           'day': 'Th'
         }, 
         {
           'code': '4', 
           'text': 'Thunderstorms', 
           'high': '88', 
           'low': '77', 
           'date': '09 Jun 2017', 
           'day': 'Fri'
         }, 
         {
           'code': '4', 
           'text': 'Thunderstorms', 
           'high': '83', 
           'low': '76', 
           'date': '10 Jun 2017', 
           'day': 'Sat'
         }], 
       'link': 'http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-1154781/', 
       'lat': '3.15248', 
       'guid': {'isPermaLink': 'false'}, 
       'condition': {'date': 'Thu, 01 Jun 2017 08:00 AM MYT', 'text': 'Mostly Cloudy', 'code': '28', 'temp': '78'}}, 
       'link': 'http://us.rd.yahoo.com/dailynews/rss/weather/Country__Country/*https://weather.yahoo.com/country/state/city-1154781/', 
       'location': {'city': 'Kuala Lumpur', 'region': ' Kuala Lumpur', 'country': 'Malaysia'}, 'ttl': '60', 'units': {'distance': 'mi', 'speed': 'mph', 'temperature': 'F', 'pressure': 'in'}, 'astronomy': {'sunset': '7:20 pm', 'sunrise': '7:2 am'}, 'wind': {'direction': '68', 'speed': '7', 'chill': '79'}}}
