import sys, os

def loadData(path, itemNum = 5):
	'''
	Load the data of FlightSpider 
	Args: data path, item number of each record (default = 5)
	Return: A dictionary of data
	'''
	searchDate = []
	record = []
	FormatData = {}

	fp = open(path, 'r')
	data = fp.readlines()
	dataNum = len(data) / (itemNum + 2)
	for i in range(dataNum):
		searchDate.append(data[i * (itemNum + 2)].split(':')[1].strip())
		for j in range(1, (itemNum + 1)):
			record.append(data[i * (itemNum + 2) + j])

	# Convert to dictionary
	for i in range(dataNum):
		for j in range(itemNum):
			speData = record[i * itemNum + j].split('\t')
			FormatData[searchDate[i]] = {}
			FormatData[searchDate[i]]['Company'] = speData[0]
			FormatData[searchDate[i]]['Punctuality'] = speData[1]
			FormatData[searchDate[i]]['Price'] = speData[2]
			FormatData[searchDate[i]]['DepartureTime'] = speData[3]
			FormatData[searchDate[i]]['FlightTime'] = speData[4]
			FormatData[searchDate[i]]['ArriveTime'] = speData[5].strip()

	return FormatData
