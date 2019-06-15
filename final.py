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
import lcd_multithread
import math
import dht as DHT
import motion
import multiprocessing as mp
from Relay import *
from motion import ispassing
from cimis import cimis
import RPi.GPIO as GPIO

localTemp = 0.0
localHum  = 0
localET   = 0.0
cimisTemp = 0.0
cimisHum  = 0
cimisET   = 0.0
r = True
savedWater = True
waterSaved = 0.0
currentHour = 0 #the most recent non-empty hour of CIMIS data
beginningHour = 0
maxLines = 100
data = []
avgET = 0.0
realTime = datetime.now()
hours = 0
minutes = 0
date = "date" #this global string holds the current date
timer_on = False
timer_seconds = 0.0
changeMessage = False

"""
timer_finish = False
timer_seconds = 0
start_timer = False
timer_pause = False
relay_on = False
"""
	#Data structure responsible for keeping track of the ET, local temp and
	#humidity for time t
class dataNode:
	def __init__(self, time, ETo, temp, humidity):
		self.time     = time
		self.ETo      = ETo
		self.temp     = temp
		self.humidity = humidity

	def setET(self, ET):
		self.ET       = ET

def Timer_Thread ():
	global timer_on
	global timer_seconds
	global minutes
	global localTemp
	global localHum
	global localET
	global cimisTemp
	global cimisHum
	global cimisET
	global savedWater
	global waterSaved
        global changeMessage
	
	timestamp = minutes
    
	while ( True ):
		sleep(0.1)
		#if timer is turned on, this means relay is to be turned on for a set time
		string = " localTemp: " + str(localTemp) + " Local Hum: " + str(localHum) + " localET: " + str(localET) + " CimisTemp: " + str(cimisTemp) + " CimisHum: " + str(cimisHum) + " CimisET: " + str(cimisET)
		if(waterSaved):
			string += " WaterSaved: " + str(waterSaved)
		else:
			string += " WaterLost: " + str(waterSaved)
		if (  timer_on ):
                        print "******************Relay is On*********************"
                        on()
			#get target time and current time
			begin = time.time()
                        tcurrent = begin
			while(True):				
				if(tcurrent - begin >= timer_seconds):
					timer_on = False
					off()
                                        print "************************************* Shutting off relay ***********************"
					break
                        #        else:
                        #            on()
			        
				motion_sensor_lock.acquire()
				if ( not motion_sensor_queue.empty() ):
					ispassing = motion_sensor_queue.get()
				motion_sensor_lock.release()
				
				if ( ispassing):
					print "************************************8 Registered Movement and am now turning off Relay ******************************88"
					tempStr = "Someone has been detected.  Turning Off"
                                        lcd_multithread.updateString(tempStr)
					off()
					sleep(1.5)
                                        lcd_multithread.updateString(string)
					timer_seconds += 1.6
				else:
					on()
				
                                sleep(0.1)
				tcurrent = time.time() #update tcurrent at the end of every loop
		if(timestamp != minutes and changeMessage):
			timestamp = minutes
                        print string
                        lcd_multithread.updateString(string)
                        changeMessage = False
        print "Timer exited both Fucking LOOPS!!!!!!!!!!!!!!!!!!!!!!!!!"

"""
def Timer_Thread ():
    global start_timer
    global timer_seconds
    global timer_finish
    global timer_pause

    while ( True ):
        sleep(0.1)
        count = timer_seconds
        if ( start_timer ):
            while ( count > 0 ):
                print("Timer is starting+++++++++++")
                sleep(0.5)
                while ( timer_pause ):
                    continue
                sleep(0.5)
                count = count - 1
            print ("Timer is ending+++++++++++++++++++")
            timer_finish = True
            start_timer = False
"""

def Update( lTemp, lHumidity, lET ):
	global date
	global currentHour
	global cimisTemp
	global cimisHum
	global cimisET
	global savedWater
	global waterSaved
	global hours
	global timer_seconds
        global timer_on
	#global relay_on

	cimis_data = None
	averageTemp = lTemp / 60.0    #once update is called, average the locally collected data
	averageHumidity = lHumidity / 60.0
	averageET = lET/60.0
	newNode = dataNode( 100, averageET, averageTemp, averageHumidity )
	data.append(newNode)

  #-----------------------------The part of the code that gets the cimis data 
        """ 
        xls_path = 'CIMIS_query.csv' # TODO: make this dep on stations/query date
        appKey = 'acac78e2-860f-4194-b27c-ebc296745833'
        sites = [75]
        month = int(datetime.today().strftime('%m'))
	day   = int(datetime.today().strftime('%d'))
	year  = int(datetime.today().strftime('%Y'))
	currentdate  = str(month) + '-' + str(day) + '-' + str(year)
        print "start date: " + date
        print "end date: " + currentdate

        interval ='hourly' #options are:    default, daily, hourly
        start = date #self-explanatory
        end = currentdate #self-explanatory

        site_names, cimis_data = cimis.run_query(appKey, sites, interval,
                                       start=start, end=end)
        #if ( cimis_data == None ):
            #Take care of failure
        csv = cimis_data[0].to_csv(index=False)
        f = open(xls_path, "w+")
        f.write(csv)
        f.close()
        """
        
  #------------------------------End of cimis data code
  
 	print("Currently Updating\n")
	count = 0
	sum = 0.0
	tempTemp = 0.0
	tempHumidity = 0
	tempET = 0.0

	with open("cimis/CIMIS_query.csv", "rt") as file: #Open CVS CIMIS File
		for line in file:
			info = line.split(",")
                        if(info[0] == 'HlyAsceEto'):
                            continue

			#stop reading the file either when we have caught up to the specified hours or when we have reaced end of CIMIS file
			if count >= (hours+beginningHour) or info[4] == "":
				break

			ETo      = float(info[9])
			temp     = float(info[13])
			humidity = int(float(info[1]))
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
				ET = ETo * float(data[index].temp/temp) * float(humidity)/float(data[index].humidity)
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
		cimisTemp = tempTemp
		cimisHum  = tempHumidity
		cimisET   = tempET
		currentHour = count
		#Calulate timing
		calculatedWater = ((avgET * 1 * 200 * 0.62)/0.75)/24
		cimisWater      = ((cimisET *1* 200 * 0.62)/0.75)/24
		if(cimisWater < calculatedWater):
			savedWater = False
                        waterSaved = calculatedWater - cimisWater
		else:
			savedWater = True
                        waterSaved = cimisWater - calculatedWater
		calculatedTime = calculatedWater/1020 * 60 * 60
                print "Calculated time: " + str(calculatedTime)
                #relay_on = True
                timer_seconds = calculatedTime + 50.0 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                timer_on  = True
	else:
		print "========= No data to report"
		cimisTemp = 0.0
		cimisHum  = 0
		cimisET   = 0.0
                waterSaved = 0.0
                timer_seconds = 10.0 #DElete this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                timer_on = True
                savedWater = False

def loop():
	global currentHour
	global beginningHour
	global realTime
	global hours
	global date
	global localTemp
	global localHum
	global localET
	global cimisTemp
	global cimisHum
	global cimisET
	global savedWater
	global waterSaved
	global minutes
        global changeMessage

	minutes = 0
	#Before actual looping starts, get current date to help with reading the file for later
	month = int(datetime.today().strftime('%m'))
	day   = int(datetime.today().strftime('%d'))
	year  = int(datetime.today().strftime('%Y'))
	date  = str(month) + '-' + str(day) + '-' + str(year)
	print date
        ispassing = False

	lTemp = 0.0
	lHumidity = 0
	lET = 0.0
	t1 = int(datetime.today().strftime('%S'))  #t1 and t2 are simply timestamps that help program know when a minute has passed
	t2 = t1

	while(hours < 24):
		sleep(1.5)
		now = realTime.now() #Get the Current real time and convert to minutes
                
		t2 = int(datetime.today().strftime('%S'))
		if t1 != t2: #Check if the minute changed and update the counter if necessary.  t1 != t2 if a minute has passed.
			t1 = t2
                        print datetime.now().strftime('%H : %M : %S')
			minutes += 1
			print "minutes: " + str(minutes)
			lET += 0.01
			localHum, localTemp = DHT.dht_GetData()
                        #localHum = 70
                        #localTemp = 70.0
                        changeMessage = True
			localET = 0.01
			lHumidity = lHumidity + localHum
			lTemp = lTemp + localTemp
			lET = + lET + localET
			
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
			date  = str(month) + '-' + str(day) + '-' + str(year)
			print date
			currentHour = int(datetime.today().strftime('%H'))
			beginningHour = currentHour

		#wait another hour to check
        turn_that_trash_off()

def turn_that_trash_off():
    destroy()
    motion.destroy()
    lcd_multithread.destroy()
    y.join()
    x.join() 
    t.join()
    GPIO.cleanup()
    exit()


if __name__=='__main__':
	print('Program is starting')
	#global currentHour
	#global beginningHour
	#global r
	currentHour = int(datetime.today().strftime('%H'))
        print "Current Hour: " + str(currentHour)
	beginningHour = currentHour
	"""
		This is where we shall start the thread for the LCD.
	"""

	try:
            bub = time.time()
            motion_sensor_queue = mp.Queue()
            motion_sensor_lock = mp.Lock()
            setup()
            off()
            x = threading.Thread( target = lcd_multithread.LCDprint, args=("You could not Live with your own failure. Where did that bring you? Back to me",) )
            x.daemon = True
            x.start()
            motion.setup( motion_sensor_queue, motion_sensor_lock )
            y = mp.Process(target = motion.loop, args = () )
            y.start()
            t = threading.Thread ( target = Timer_Thread, args = () )
            t.daemon = True
            t.start()
	    loop()
	except KeyboardInterrupt:
                turn_that_trash_off()
		r = False
		print "Exiting\n"
