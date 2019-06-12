#!/usr/bin/env python3
#yutong wang

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

import threading
import time

title = "BRUH:"
string = "WE LIVE in a SOCIETY, and society lives in us! "
update = False

def updateString(s):
    global string
    global update
    string = s
    update = True
    lcd.clear()
    time.sleep(1)

def str_loop(l):
    global update
    global buf
    global length
    global counter
    length = l
    counter = 15
    if length>16:
        buf = string[0:15]
        while True:
            #lcd.delayMicroseconds(200)
            #print ("loop:"+string)
            #print("counter",counter)
            lcd.clear()
            lcd.message(title+'\n')
            lcd.message(buf)
            time.sleep(0.3)
            buf = buf[1:] + string[counter]
            counter+=1
            if counter>=length:
                counter=0
            if update:
                counter=15
                buf = string[0:15]
                length = len(string)
                update = False
    else:
        buf = string
        lcd.message(title+'\n')
        lcd.message(string)


def LCDprint(s):
    global string
    string = s
    mcp.output(3,1) #turn on LCD backlight
    lcd.begin(16,2) #set number of LCD lines and columns
    lcd.setCursor(0,0)
    #print("string length: ")
    #print(len(string))
    str_loop(len(s))


def destroy():
    lcd.clear()


PCF8574_address = 0x27 #I2C address of PCF8574
PCF8574A_address = 0x3F #I2C address of PCF8574A

try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print("I2C Address Error !")
        exit(1)
#create LCD, passing in MCP GPIO adapter
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
"""
x = threading.Thread(target=LCDprint,args=(string,))
x.start()
time.sleep(3)
print("wake up")
updateString("bufer is working yay buffer is working !!")
time.sleep(5)
print("wake up")
updateString("MERP MERP MERP MERP MERP MERP")
x.join()
"""
