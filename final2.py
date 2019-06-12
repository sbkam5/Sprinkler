#!python2
#############################################################################
# Creator: Spencer Brendan Kam
# Date Created: idk, go ask him
# Last Modified: 06/5/2019
# Description: Module responsible for updating the CIMIS and local data
# Revisions: Added timing functionality and comment for easier readability
#  			 Also removed dependencies on previous inputs
#			 Separated and modularized
# Additional Comments:
#############################################################################

from datetime import datetime
import time
from time import sleep
import threading
import head
from test import lcd_thread

head.localTemp = 0.0
head.localHum  = 0
head.localET   = 0.0
head.cimisTemp = 0.0
head.cimisHum  = 0
head.cimisET   = 0.0
head.r = True

currentHour = 0 #the most recent non-empty hour of CIMIS data
beginningHour = 0
maxLines = 100
data = []
avgET = 0.0
realTime = datetime.now()
hours = 0
date = "date" #this global string holds the current date

"""
	Data structure responsible for keeping track of the ET, local temp and
	humidity for time t
"""
class dataNode:
	def __init__(self, time, ETo, temp, humidity):
		self.time     = time
		self.ETo      = ETo
		self.temp     = temp
		self.humidity = humidity

	def setET(self, ET):
		self.ET       = ET

def Update( lTemp, lHumidity, lET ):
	global date
	global currentHour
	#global head.cimisTemp
	#global head.cimisHum
	#global head.cimisET

	averageTemp = lTemp / 60.0    #once update is called, average the locally collected data
	averageHumidity = lHumidity / 60.0
	averageET = lET/60.0
	newNode = dataNode( 100, averageET, averageTemp, averageHumidity )
	data.append(newNode)
	found = 0 #This is a variable that turns to 1 once the first element of the date of interest is found.

	print("Currently Updating\n")
	count = 0
	sum = 0.0
	tempTemp = 0.0
	tempHumidity = 0
	tempET = 0.0

	with open("hourly075.csv", "rt") as file: #Open CVS CIMIS File
		for line in file:
			info = line.split(",")
			if info[1] != date and found == 0:  #Skip through lines in file till you get to date of interest.  Once found, found = 1.
				continue
			else:
				found = 1

			#stop reading the file either when we have caught up to the specified hours or when we have reaced end of CIMIS file
			if count >= (hours+beginningHour) or info[4] == "--":
				break

			CimisTime     = int(info[2])
			ETo      = float(info[4])
			temp     = float(info[12])
			humidity = int(info[14])
			tempTemp = temp
			tempHumidity = humidity
			tempET = ETo
			count += 1 #increment count everytime there is an entry that isnt empty

			#print "-----Index: %d" %(count)
			#print "ETo: " + str(ETo)
			#print "temp: " + str(temp)
			#print "humidity: " + str(humidity)

			#If a new entry has info, we can use that to calculate the ET
			if count > currentHour:
				index = count - currentHour-1
				ET = data[index].ETo * float(data[index].temp/temp) * float(humidity)/float(data[index].humidity)
				data.pop(index)
				sum += ET

	#CurrentSize holds the length of what the CIMIS data is/was supposed to be,
	#so if count > currentSize, this means new data has been added to CIMIS file.
	if(currentHour < count):
		#Calculate average ET.
		avgET = float(sum/(count-currentHour))
		print "========= Average: %f" %(avgET)
		print "========= Hours calc'ed for: %d" %(count-currentHour)
		print "========= Size of local: %d" %(len(data))
		head.cimisTemp = tempTemp
		head.cimisHum  = tempHumidity
		head.cimisET   = tempET
		currentHour = count
	else:
		print "========= No data to report"
		cimisTemp = 0.0
		cimisHum  = 0
		cimisET   = 0.0

def loop():
	global currentHour
	global beginningHour
	global realTime
	global hours
	global date
	#global head.localTemp
	#global head.localHum
	#global head.localET
	#Before actual looping starts, get current date to help with reading the file for later
	month = int(datetime.today().strftime('%m'))
	day   = int(datetime.today().strftime('%d'))
	year  = int(datetime.today().strftime('%Y'))
	date  = str(month) + '/' + str(day) + '/' + str(year)
	print date


	lTemp = 0.0
	lHumidity = 0
	lET = 0.0
	minutes = 0
	t1 = int(datetime.today().strftime('%S'))  #t1 and t2 are simply timestamps that help program know when a minute has passed
	t2 = t1

	while(hours < 24):
		sleep(0.01)
		now = realTime.now() #Get the Current real time and convert to minutes
		t2 = int(datetime.today().strftime('%S'))
		if t1 != t2: #Check if the minute changed and update the counter if necessary.  t1 != t2 if a minute has passed.
			t1 = t2
			minutes += 1
			#print "minutes: " + str(minutes)
			lTemp += 70.0 #Static Testing Values
			lHumidity += 70 #Static Testing Values
			lET += 0.01
			head.localTemp = 70.0
			head.localHum = 70
			head.localET = 0.01

		if minutes >= 60: #If the minute tracker has reached 60 (an hour) -> update
			print "------------- It's been an hour ----------------"
			hours += 1
			minutes = 0
			Update( lTemp, lHumidity, lET ) #Run calculations and Update CIMIS
			lTemp = 0.0
			lHumidity = 0
			lET = 0.0

		#if hours becomes >= 24, reset it, currentHour, beginningHour, and date after updating LCD and calling update.
		if hours >= 24:
			print "====== Reseting ======"
			hours = 0
			month = int(datetime.today().strftime('%m'))
			day   = int(datetime.today().strftime('%d'))
			year  = int(datetime.today().strftime('%Y'))
			date  = str(month) + '/' + str(day) + '/' + str(year)
			print date
			currentHour = int(datetime.today().strftime('%H'))
			beginningHour = currentHour

		#wait another hour to check



if __name__=='__main__':
	print('Program is starting')
	global currentHour
	global beginningHour
	#global head.r
	currentHour = int(datetime.today().strftime('%H'))
	beginningHour = currentHour
	"""
		This is where we shall start the thread for the LCD.
	"""

	try:
		t = threading.Thread(target=lcd_thread)
		t.daemon = True
		t.start()
		loop()
	except KeyboardInterrupt:
		head.r = False
		t.join()
		print "Exiting\n"
	
