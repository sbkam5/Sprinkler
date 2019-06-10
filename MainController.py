#!python2
#############################################################################
# Creator: Manuel Macedonio Alvarez
# Date Created: 06/05/2019
# Last Modified: 06/05/2019
# Description: Primary Control Center. Mainloop will track time, interrupts,
#              Input and Output
# Revisions:
# Additional Comments:
#############################################################################

from datetime import datetime
import time as clock
import final as Final
import threading as t
from lcd import LCDprint

#functionality for the timer.
timer_finished = True #Determines whether timer is running
seconds = 0.5 #Predetermined wait time for the timer
motion_sensor_detect = False #Bool to determine if someone is present
current_time = datetime.now()
timer_wait = True

#Threading Function for the Timer
def Timer ():
    global timer_finished
    global seconds
    global stall
    global count

    while ( True ):
        stall = True
        print("Timer Start")
        clock.sleep(seconds) #Timer is Running
        timer_finished = True
        while ( timer_wait ): #Wait for Signal from Main Controller to reset timer
            continue

def Minute_Reset():
    time = current_time.now() #Get the Current Time
    current_minutes = int (time.strftime("%S"))
    minute_counter = 60 - current_minutes #Reset the Minute Counter for the next hour
    return minute_counter

#Main Controller. Loop and Data Signals
def Controller():
    global timer_finished
    global motion_sensor_detect
    global current_time
    global stall
    global count
    minute_counter = Minute_Reset() #Keeps track of how many minutes left until an hour
    hours = 0

    Timer_Thread = t.Thread(target=Timer)
    Timer_Thread.daemon = True
    Timer_Thread.start()

    #Main Loop
    while ( hours < 24 ): #Run for twenty four hours

        timer_finished = False #Global Variable to indicate that the timer is currently running
        clock.sleep(0.25)

        while ( not timer_finished and not motion_sensor_detect ): #Wait for Timer or Motion Sensor Interrupt
            #Have LCD do something, so we're not busy waiting
            continue

        if ( timer_finished ): #Timer Finished
            print("Timer Finished\n")
            minute_counter = minute_counter - 1 #Decrement Current Minutes
            print("Minutes Remaining: " + str(minute_counter))
            #Read Temperature and Sensor Data

            if ( minute_counter == 0 ): #If time reaches an hour, update values
                print("Hour Complete: Updating and Reseting")
                ET, averageTemp, averageHumidity = Final.Update(10, 15) #Call the Update Function
                minute_counter = Minute_Reset() #Reset the amount of minutes left for an hour
                hours = hours + 1
                LCDprint( str(realTime.now()) + "\nET: " + str(ET) + "Average Temperature: " + str(averageTemp) +
                            "*C averageHumidity: " + str(averageHumidity))

            timer_wait = False #Signal the Timer thread to restart

        elif ( motion_sensor_detect ): #Motion Sensor detected movement
            print("Some dumbass walked into the path. Probably Spencer")
            print("Turning off Relay")
            motion_sensor_detect = False

    print("24 Hours have passed. Shutting down system\n")
    exit()

#Main Function Used to Initalize the Program
def main():
    print("Starting Sprinkler Control System")
    try:
        print("Entering Timer Loop")
        Controller()
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt Shutdown Signal")
        print("Exiting Program"
        )
if __name__ == '__main__':
    main()
