import re
import urllib, urllib2
import datetime, time
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
	allTime = re.compile('<em class="number">(.*?)</em>').findall(html)


	depTime = []; fliTime = []; lanTime = []
	#Classify the time
	timeFlag = 0
	for item in allTime:
		if 'h' in item:
			fliTime.append(item)
		elif ':' in item and timeFlag == 1:
			lanTime.append(item)
			timeFlag = 0 
		elif ':' in item and timeFlag == 0:
			depTime.append(item)
			timeFlag = 1
	
	info = []
	if len(company) > num-2 and len(punctuality) > num-2 and len(price) > num-2 and len(depTime) > num-2:
		for i in range(num):
			if '%' not in punctuality[i]:
				punctuality[i] = 'NAN'
			info.append([company[i], punctuality[i], price[i], depTime[i], fliTime[i], lanTime[i]])
	return info

def dataRecord(flightDate, recordNum, fromCity, toCity):
	'''
	Record the information each day until the flight
	Args:  flight date, record number, fromCity, toCity
	Return: None
	'''
	today = time.strftime('%Y-%m-%d')
	y, m, d = today.split('-')
	fy, fm, fd = flightDate.split('-')
	while True:
		# Search
		url = searchUrl(fromCity, toCity, flightDate)
		info = searchInfo(url, recordNum)

		# Save to file
		filename = flightDate + '_' + fromCity + '_' + toCity + '.txt'
		output = open(filename, 'a')
		temp = 'SearchDate: ' + today + '\n'
		for item in info:
			temp += item[0] + '\t' + item[1] + '\t' + item[2] + '\t' + item[3] + '\t' + item[4] + '\t' + item[5] + '\n'
		temp += '\n'
		output.writelines(temp)
		output.close()
		print today , ': Information Record!'

		# Time to stop. Planes are taking off!
		y, m, d = today.split('-')
		if y == fy and m == fm and d == fd:
			break

		# Sleep until tomorrow
		while today.split('-')[2] == d:
			time.sleep(600)
			today = time.strftime('%Y-%m-%d')
