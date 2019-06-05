from datetime import datetime
import time

currentSize = 0 #of CIMIS data
maxLines = 100
data = []
avgET = 0.0
realTime = datetime.now()
hours = 0

class dataNode:
	def __init__(self, time, ETo, temp, humidity):
		self.time     = time
		self.ETo      = ETo
		self.temp     = temp
		self.humidity = humidity
		
	def setET(self, ET):
		self.ET       = ET
	

def loop():
	global currentSize
	global realTime
	global hours
	localTemp = 0.0
	localHumidity = 0
	minutes = 0

	while(currentSize < 10):
		#First Get the local humidity and temp. Store into data structure
		#newNode = dataNode(l_time, l_ETo, l_temp, l_humidity)
		now = realTime.now()
		currentMinutes = int(now.strftime("%S"))
		if currentMinutes != minutes:
			#print "Adding a minute"
			minutes += 1
			localTemp += 70.0
			localHumidity += 70

		if minutes == 60:
			hours += 1
			minutes = 0
			averageTemp = localTemp/60.0
			localTemp = 0.0
			averageHumidity = localHumidity/60
			localHumidity = 0
			newNode = dataNode(100, 0.01, averageTemp, averageHumidity)
			data.append(newNode)
	
			#Next get data from CIMIS and read the resulting file
			count = 0
			sum   = 0.0
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
						#data[index].setET(ET)
						data.pop(index)
						sum += ET
			
			#CurrentSize holds the length of what the CIMIS data is/was supposed to be, so if count > currentSize, this means new data has been added to CIMIS file.
			if(currentSize < count):
				#Calculate average ET.
				avgET = float(sum/(count-currentSize))
				print "========= Average: %f" %(avgET)
				print "========= Hours calc'ed for: %d" %(count-currentSize)
				print "========= Size of local: %d" %(len(data))
				currentSize = count
			#minutes is rest always	
			minutes = 0
		
			
		#wait another hour to check
		#time.sleep(2)
		#print "Waited"
			

if __name__=='__main__':
	print('Program is starting')
	
	
	try:
		loop()
	except KeyboardInterrupt:
		print "Exiting\n"
