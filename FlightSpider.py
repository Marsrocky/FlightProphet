import re
import urllib, urllib2
import datetime
from CityAirport import *

def searchUrl(fromCity, toCity, startdate):
	'''
	Get the url for searching
	Args: Flight from one city to another on specific date
	Example:
		fromCity(Jinan), toCity(Beijing), startdate(2015-6-24)
	Returns: Url
	'''
	dcity = CityAirport[fromCity]
	acity = CityAirport[toCity]

	year, month, day = startdate.split('-')
	weekday = WeekDay[int(datetime.datetime(int(year), int(month), int(day)).strftime("%w"))]
	searchUrl = 'http://english.ctrip.com/chinaflights/' + fromCity + '--to-' + toCity + '-/tickets-' + dcity + '-' + acity + '/?flighttype=s&dcity=' + dcity + '&acity=' + acity + '&startdate=' + startdate + '&startday=' + weekday + '&searchboxArg=t'
	return searchUrl

def searchInfo(searchUrl, num):
	'''
	Get the information of the flight (specific info num)
	Args: Specific url, Number
	Return: dictionary of information:
		[Company, Punctuality, Price]
	'''
	html = urllib2.urlopen(searchUrl).read()
	company = re.compile('<div class="flightAirline" title="(.*?)">').findall(html)
	punctuality = re.compile('<div class="b_sumArea">(.*?)</div>').findall(html)
	price = re.compile('class="price"><dfn>CNY</dfn><strong class="number">(.*?)</strong>').findall(html)
	info = []
	if len(company) > num-2 and len(punctuality) > num-2 and len(price) > num-2:
		for i in range(num):
			if '%' not in punctuality[i]:
				punctuality[i] = 'NAN'
			info.append([company[i], punctuality[i], price[i]])
	return info
