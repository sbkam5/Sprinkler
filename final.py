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

currentSize = 0 #of CIMIS data
maxLines = 100
data = []
avgET = 0.0
realTime = datetime.now()
hours = 0

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

def Update( localTemp, localHumidity ):
	global currentSize
	averageTemp = localTemp / 60.0
	averageHumidity = localHumidity / 60.0
	newNode = dataNode( 100, 0.01, averageTemp, averageHumidity )
	data.append(newNode)

	print("Currently Updating\n")
	count = 0
	sum = 0.0

	with open("hourly075.csv", "rt") as file:
		for line in file:
			info = line.split(",")
			#stop reading the file either when we have caught up to the specified hours or when we have reaced end of CIMIS file
			if count >= hours or info[4] == "--":
				break

			CimisTime     = int(info[2])
			ETo      = float(info[4])
			temp     = float(info[12])
			humidity = int(info[14])
			count += 1 #increment count everytime there is an entry that isnt empty

			print "-----Index: %d" %(count)
			print "ETo: " + str(ETo)
			print "temp: " + str(temp)
			print "humidity: " + str(humidity)

			#If a new entry has info, we can use that to calculate the ET
			if count > currentSize:
				index = count - currentSize - 1
				ET = data[index].ETo * float(data[index].temp/temp) * float(humidity)/float(data[index].humidity)
				data.pop(index)
				sum += ET

			#CurrentSize holds the length of what the CIMIS data is/was supposed to be,
			#so if count > currentSize, this means new data has been added to CIMIS file.
			if(currentSize < count):
				#Calculate average ET.
				avgET = float(sum/(count-currentSize))
				print "========= Average: %f" %(avgET)
				print "========= Hours calc'ed for: %d" %(count-currentSize)
				print "========= Size of local: %d" %(len(data))
				currentSize = count

def loop():
	global currentSize
	global realTime
	global hours
	localTemp = 0.0
	localHumidity = 0
	minutes = 0

	while(currentSize < 10):
		now = realTime.now() #Get the Current real time and convert to minutes
		currentMinutes = int(now.strftime("%S"))
		if currentMinutes != minutes: #Check if the minute changed and update the counter if necessary
			minutes += 1
			localTemp += 70.0 #Static Testing Values
			localHumidity += 70 #Static Testing Values

		if minutes == 60: #If the minute tracker has reached 60 (an hour) -> update
			hours += 1
			minutes = 0
			Update( localTemp, localHumidity ) #Run calculations and Update CIMIS

		#wait another hour to check


if __name__=='__main__':
	print('Program is starting')


	try:
		loop()
	except KeyboardInterrupt:
		print "Exiting\n"
