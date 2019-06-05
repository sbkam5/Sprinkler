import time

currentSize = 0
maxLines = 100
data = []
avgET = 0.0

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
	while(currentSize < 10):
		#First Get the local humidity and temp. Store into data structure
		#newNode = dataNode(l_time, l_ETo, l_temp, l_humidity)
		newNode = dataNode(100, 0.01, 70.0, 70)
		data.append(newNode)
	
		#Next get data from CIMIS and read the resulting file
		count = 0
		sum   = 0.0
		with open("hourly075.csv", "rt") as file:
			for line in file:
				info = line.split(",")
				if count >= len(data):
					break
			
				if info[4] == "--":
					break
				
				currentTime     = info[2]
				ETo      = float(info[4])
				temp     = float(info[12])
				humidity = info[14]

				print "-----Index: %d" %(count)
				print "ETo: " + str(ETo)
				print "temp: " + str(temp)
				print "humidity: " + str(humidity)
			
				#If a new entry has info, we can use that to calculate the ET
				ET = data[count].ETo * float(data[count].temp/temp) * float(humidity)/float(data[count].humidity)
				data[count].setET(ET)
			
				sum += ET
				count+=1  #increment count everytime there is a new entry that isnt empty
			
		
		#Calculate average ET.
		avgET = float(sum/count)
		print "========= Average: %f" %(avgET)
			
		#update currentSize to reflect how many CIMIS entries we have now completed.
		if(currentSize < count):
			currentSize = count
		
			
		#wait another hour to check
		time.sleep(2)
		print "Waited"
			

if __name__=='__main__':
	print('Program is starting')
	
	
	try:
		loop()
	except KeyboardInterrupt:
		print "Exiting\n"
